@description('Location for all resources.')
param location string = resourceGroup().location

@description('Azure Container Registry server (e.g. myregistry.azurecr.io)')
param acrServer string

@description('Container image tag to deploy')
param imageTag string = 'latest'

@description('Azure OpenAI endpoint')
param azureOpenAiEndpoint string

@description('Foundry project endpoint')
param foundryProjectEndpoint string

@description('Azure AI Search endpoint')
param azureSearchEndpoint string

@description('Microsoft Fabric workspace ID')
param fabricWorkspaceId string

var tags = {
  project: 'autonomous-finance-copilot'
}

// ── Key Vault ─────────────────────────────────────────────────────────────────
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: 'kv-afc-${uniqueString(resourceGroup().id)}'
  location: location
  tags: tags
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 90
  }
}

// ── Azure AI Search ───────────────────────────────────────────────────────────
resource aiSearch 'Microsoft.Search/searchServices@2023-11-01' = {
  name: 'srch-afc-${uniqueString(resourceGroup().id)}'
  location: location
  tags: tags
  sku: {
    name: 'standard'
  }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
  }
}

// ── Container Apps environment ────────────────────────────────────────────────
resource containerAppsEnv 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: 'cae-afc-${uniqueString(resourceGroup().id)}'
  location: location
  tags: tags
  properties: {}
}

// ── Container App ─────────────────────────────────────────────────────────────
resource containerApp 'Microsoft.App/containerApps@2024-03-01' = {
  name: 'ca-afc-${uniqueString(resourceGroup().id)}'
  location: location
  tags: tags
  properties: {
    managedEnvironmentId: containerAppsEnv.id
    configuration: {
      ingress: {
        external: true
        targetPort: 8000
      }
      registries: [
        {
          server: acrServer
          identity: 'system'
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'autonomous-finance-copilot'
          image: '${acrServer}/autonomous-finance-copilot:${imageTag}'
          resources: {
            cpu: json('1.0')
            memory: '2Gi'
          }
          env: [
            {
              name: 'AZURE_OPENAI_ENDPOINT'
              value: azureOpenAiEndpoint
            }
            {
              name: 'FOUNDRY_PROJECT_ENDPOINT'
              value: foundryProjectEndpoint
            }
            {
              name: 'AZURE_SEARCH_ENDPOINT'
              value: azureSearchEndpoint
            }
            {
              name: 'FABRIC_WORKSPACE_ID'
              value: fabricWorkspaceId
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 3
      }
    }
  }
  identity: {
    type: 'SystemAssigned'
  }
}

// ── Outputs ───────────────────────────────────────────────────────────────────
output containerAppFqdn string = containerApp.properties.configuration.ingress.fqdn
output keyVaultName string = keyVault.name
output searchServiceName string = aiSearch.name
