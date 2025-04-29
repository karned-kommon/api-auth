# keycloack

Il est nécessaire d'ajouter manuellement votre audience via l'interface de Keycloack.
Source : https://stackoverflow.com/questions/53550321/keycloak-gatekeeper-aud-claim-and-client-id-do-not-match

## Configure audience in Keycloak
- Add realm or configure existing
- Add client my-app or use existing

Goto to the newly added "Client Scopes" menu [1]
- Add Client scope 'good-service'

Within the settings of the 'good-service' goto Mappers tab
- Create Protocol Mapper 'my-app-audience' 
  - Name: my-app-audience
  - Choose Mapper type: Audience
  - Included Client Audience: my-app
  - Add to access token: on

Configure client my-app in the "Clients" menu
Client Scopes tab in my-app settings
- Add available client scopes "good-service" to assigned default client scopes

If you have more than one client repeat the steps for the other clients as well and add the good-service scope. 
The intention behind this is to isolate client access. The issued access token will only be valid for the intended audience.
This is thoroughly described in Keycloak's documentation [1,2].

## Configure new API 
Go to https://iam.karned.bzh or keycloak admin interface
- select karned realm
- select clients
- create new client
- client id: api-credential (for example)
- client protocol: openid-connect
- next ... next ... save

- select the new client
- select the "Roles" tab
- add role create (for example)
- save

- open groups
- select existant group or create new group
- add role to group : go to "Role Mappings" tab
- select the role you want to add
- click "Assign role"
- select the role
- click "Assign"