import yaml
import os

def agenttemplate(template_name, label, image_name, vm_size, os_type, executor_count=1):
    return {
        "agentLaunchMethod": "SSH",
        "credentialsId": "oeadmin-credentials",
        "diskType": "managed",
        "doNotUseMachineIfInitFails": True,
        "enableMSI": False,
        "enableUAMI": False,
        "ephemeralOSDisk": False,
        "executeInitScriptAsRoot": True,
        "existingStorageAccountName": os.environ['STORAGE_ACCOUNT_NAME'],
        "imageReference": {
            "id": os.environ['AGENTS_IMAGE_PREFIX'] + image_name
        },
        "imageTopLevelType": "advanced",
        "initScript": "gpasswd -a oeadmin docker \n chmod g+rw /var/run/docker.sock" if os_type is "Linux" else "",
        "installDocker": False,
        "installGit": False,
        "installMaven": False,
        "jvmOptions": "-Dhudson.TcpSlaveAgentListener.hostName=" + os.environ['JENKINS_PRIVATE_IP'],
        "labels": label,
        "location": os.environ['AGENTS_LOCATION'],
        "noOfParallelJobs": executor_count,
        "osDiskSize": 0 if os_type is "Linux" else 200,
        "osType": os_type,
        "preInstallSsh": True,
        "retentionStrategy": {"azureVMCloudRetentionStrategy": {"idleTerminationMinutes": 5}},
        "shutdownOnIdle": False,
        "storageAccountNameReferenceType": "existing",
        "storageAccountType": "Standard_LRS",
        "subnetName": os.environ['SUBNET_NAME'],
        "templateDisabled": False,
        "templateName": template_name,
        "usageMode": "Only build jobs with label expressions matching this node",
        "usePrivateIP": True,
        "virtualMachineSize": vm_size,
        "virtualNetworkName": os.environ['VNET_NAME'],
        "virtualNetworkResourceGroupName": os.environ['JENKINS_RESOURCE_GROUP']
    }


def usernamePassword(id, description, username, password):
    return {
        "usernamePassword": {
            "description": description,
            "id": id,
            "username": username,
            "password": password,
            "scope": "GLOBAL"
        }
    }


def azureStorageAccount(id, description, name, key):
    return {
      "azureStorageAccount": {
          "blobEndpointURL": "https://blob.core.windows.net/",
          "description": description,
          "id": id,
          "scope": "GLOBAL",
          "storageAccountName": name,
          "storageKey": key
      }
    }


def stringCreds(id, description, secret):
    return {
        "string": {
            "description": description,
            "id": id,
            "scope": "GLOBAL",
            "secret": secret
        }
    }


def azureCredentials(id, description, clientId, clientSecret, subscriptionId, tenant):
    return {
        "azure": {
            "azureEnvironmentName": "Azure",
            "clientId": clientId,
            "clientSecret": clientSecret,
            "description": description,
            "id": id,
            "scope": "GLOBAL",
            "subscriptionId": subscriptionId,
            "tenant": tenant
        }
    }


try:
    accAzureVM = {
        "azureCredentialsId": os.environ['AZURE_PRINCIPAL_ID'],
        "cloudName": os.environ['ACC_CLOUD_NAME'],
        "configurationStatus": "pass",
        "deploymentTimeout": 1200,
        "existingResourceGroupName": os.environ['JENKINS_RESOURCE_GROUP'],
        "maxVirtualMachinesLimit": 20,
        "resourceGroupReferenceType": "existing",
        "vmTemplates": [
            agenttemplate("accxenial", "ACC-1604", "terraform-xenial", "Standard_DC4s", "Linux"),
            agenttemplate("accbionic", "ACC-1804", "terraform-bionic", "Standard_DC4s", "Linux"),
            agenttemplate("ubuntunonsgx", "nonSGX", "terraform-ubuntu-nonSGX", "Standard_F8s_v2", "Linux", 4),
            agenttemplate("accwin2016", "SGXFLC-Windows", "terraform-win2016", "Standard_DC4s", "Windows"),
            agenttemplate("accwin2016dcap", "SGXFLC-Windows-DCAP", "terraform-win2016-dcap", "Standard_DC4s",
                          "Windows"),
            agenttemplate("winnonsgx", "nonSGX-Windows", "terraform-win2016-nonSGXdcap", "Standard_F8s_v2", "Windows"),
        ]
    }

    credentials = [
        azureCredentials("VMSSPrincipal", "Azure Service Principal credentials",
                         os.environ['ARM_CLIENT_ID'], os.environ['ARM_CLIENT_SECRET'],
                         os.environ['ARM_SUBSCRIPTION_ID'], os.environ['ARM_TENANT_ID']),
        azureStorageAccount("oe_jenkins_storage_account_westeurope",
                            "The storage account from the OE-Jenkins-CI-westeurope resource group (in the OSTC Lab subscription)",
                            os.environ['STORAGE_NAME_WESTEUROPE'], os.environ['STORAGE_KEY_WESTEUROPE']),
        azureStorageAccount("oe_jenkins_storage_account",
                            "The storage account from the OE-Jenkins-CI resource group (in the OSTC Lab subscription)",
                            os.environ['STORAGE_NAME_EASTUS'], os.environ['STORAGE_KEY_EASTUS']),
        usernamePassword("oeadmin-credentials", "Jenkins user password", "oeadmin",
                         "{AQAAABAAAAAgXsGuIKfm8KgMmZrJfOCL300GNJ7NQ5s9OuPp60M5SG4i0iasMrAjWE9whQgaJ3VO}"),
        usernamePassword("oe-ci", "", "oe-ci",
                         "{AQAAABAAAAAwIQWNCCLi9YTaOc5It8rHmAU/0RaJPXD4AcrWQgwqgdqoCf2Km50Y2ByQ3Aksfi3Mq+qEB0kmuWS38dgyjRgqrA==}"),
        usernamePassword("oejenkinscidockerregistry", "Creds for oe jenkins ci docker registry",
                         "oejenkinscidockerregistry",
                         "{AQAAABAAAAAwBDwKL7ZcFauHQdXnj3HNImosxT5zK2sfp4QXB+/AIpvwyqLzN7zpmlSb24kPLwg01rMw83MlFKmu8yv0mJtuhQ==}"),
        usernamePassword("oeciteamdockerhub", "oeciteam Dockerhub credentials",
                         "oeciteam",
                         "{AQAAABAAAAAQZ0nwErpj++LJ4rVyUsf/tSMrgEER7T4zFxS3j3l2CCI=}"),
        usernamePassword("SERVICE_PRINCIPAL_OSTCLAB", "SERVICE_PRINCIPAL_OSTCLAB",
                         os.environ['ARM_CLIENT_ID'], os.environ['ARM_CLIENT_SECRET']),
        stringCreds("OSCTLabSubID", "OSCTLabSubID", os.environ['ARM_SUBSCRIPTION_ID']),
        stringCreds("TenantID", "TenantID", os.environ['ARM_TENANT_ID'])
    ]

    config = {
        "credentials": {
            "system": {
                "domainCredentials": [
                    {
                        "credentials": credentials
                    }
                ]
            }
        },
        "jenkins": {
            "clouds": [
                {
                    "azureVM": accAzureVM
                }
            ],
            "numExecutors": 2,
        },
        "unclassified": {
            "globalLibraries": {
                "libraries": [
                    {
                        "allowVersionOverride": False,
                        "defaultVersion": "master",
                        "name": "OpenEnclaveCommon",
                        "retriever": {
                            "modernSCM": {
                                "scm": {
                                    "github": {
                                        "configuredByUrl": True,
                                        "credentialsId": "oe-ci",
                                        "id": "b0b743d4-7fd3-4786-bdfe-1a1df742a001",
                                        "repoOwner": "openenclave",
                                        "repository": "openenclave-ci",
                                        "repositoryURL": "https://github.com/openenclave/openenclave-ci",
                                        "traits": [
                                            {
                                                "gitHubBranchDiscovery": {
                                                    "strategyId": 1
                                                }
                                            },
                                            {
                                                "originPullRequestDiscoveryTrait": {
                                                    "strategyId": 1
                                                }
                                            },
                                            {
                                                "gitHubForkDiscovery": {
                                                    "strategyId": 1,
                                                    "trust": "gitHubTrustPermissions"
                                                }
                                            }

                                        ]

                                    }
                                }
                            }
                        }
                    }
                ]
            },
            "location": {
                "adminAddress": "oeciteam@microsoft.com",
                "url": os.environ['JENKINS_URL']
            }
        },
        "tool": {
            "git": {
                "installations": [
                    {
                        "home": "git",
                        "name": "Default"
                    }
                ]
            }
        }
    }

    with open('jenkins-config.yml', 'w') as outfile:
        yaml.safe_dump(config, outfile, default_style=None, default_flow_style=False)
except KeyError as e:
    print(e.args[0], "Environment variable is not set")
