# %%
from websocket import create_connection, WebSocketException
import json
import time

class VtubeStudioAdapter:
    
    def __init__(self):
        self.pre_hotkeyId = None
        self.ws_url = "ws://localhost:8001"
        self.connect_websocket()
        if self.ws:
            self.authentication_token = self._request_authentication_token()
            if self.authentication_token:
                authenticated = self._request_authentication(self.authentication_token)
            else:
                authenticated = False
            print(authenticated)
            
    def connect_websocket(self):
        try:
            self.ws = create_connection(self.ws_url)
        except WebSocketException as e:
            print(f"WebSocket connection error: {e}")
            self.ws = None

    def _request_authentication_token(self):
        authentication_token_request = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "TokenRequestID",
            "messageType": "AuthenticationTokenRequest",
            "data": {
                "pluginName": "expression_plugin",
                "pluginDeveloper": "master",
                "pluginIcon": None
            }
        }
        self.ws.send(json.dumps(authentication_token_request))
        response = self.ws.recv()
        print("Received '%s'" % response)
        json_response = json.loads(response)
        if json_response['messageType'] == 'AuthenticationTokenResponse':
            AuthenticationToken = json_response["data"]["authenticationToken"]
            print(f"Token: {AuthenticationToken}")
        else:
            AuthenticationToken = None
        return AuthenticationToken
        
    def _request_authentication(self,authenticationToken):
        authentication_request = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "AuthenticationRequestID",
            "messageType": "AuthenticationRequest",
            "data": {
                "pluginName": "expression_plugin",
                "pluginDeveloper": "master",
                "authenticationToken": authenticationToken
            }
        }
        self.ws.send(json.dumps(authentication_request))
        response = self.ws.recv()
        print("Received '%s'" % response)
        json_response = json.loads(response)
        if json_response['messageType'] == 'AuthenticationResponse':
            return json_response["data"]["authenticated"]
        else:
            return False

    def send_request(self, hotkeyId):
        print("hotkeyId:",hotkeyId)
        print("pre_hotkeyId:",self.pre_hotkeyId)
        def excute(hotkeyId):
            request = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "SomeID",
                "messageType": "HotkeyTriggerRequest",
                "data": {
                    "hotkeyID": hotkeyId,
                    "itemInstanceID": None
                }
            }
            request = json.dumps(request)
            self.ws.send(request)
            response = self.ws.recv()
            print("Received '%s'" % response)
        
        if not self.pre_hotkeyId:
            excute(hotkeyId)
            self.pre_hotkeyId = hotkeyId
        elif self.pre_hotkeyId == hotkeyId:
            print("pass")
            pass
        else:
            excute(self.pre_hotkeyId)
            excute(hotkeyId)
            self.pre_hotkeyId = hotkeyId

    def close_websocket(self):
        self.ws.close()
        self.ws = None
        pass

    def _is_connected(self):
        return self.ws and self.ws.connected

    def ensure_connection(self):
        #if not self._is_connected():
        #    print("WebSocket is disconnected. Attempting to reconnect...")
        self.connect_websocket()
        if self.ws:
            authenticated = self._request_authentication(self.authentication_token)
            print(authenticated)

if __name__ == "__main__":
    vs = VtubeStudioAdapter()
    i = 1
    for hotkeyId in ["23883dccdeb2425799738ec84114aef5", "e690e99696ff43d68539a387cd15d039", "e690e99696ff43d68539a387cd15d039", "91a1e2fe72bf4ef2810222d8dcde00cb", "23883dccdeb2425799738ec84114aef5"]:
        print("i = ",i)
        vs.ensure_connection()
        print("connection ok")
        vs.send_request(hotkeyId)
        print("hotkey ok")
        time.sleep(10)
        i += 1
    

"""
# Expression file active/deactive list
{
	"apiName": "VTubeStudioPublicAPI",
	"apiVersion": "1.0",
	"requestID": "SomeID",
	"messageType": "ExpressionStateRequest",
	"data": {
		"details": true,
		"expressionFile": "myExpression_optional_1.exp3.json",
	}
}

# Expression file active/deactive trigger
{
	"apiName": "VTubeStudioPublicAPI",
	"apiVersion": "1.0",
	"requestID": "SomeID",
	"messageType": "ExpressionActivationRequest",
	"data": {
		"expressionFile": "myExpression_1.exp3.json",
		"active": true
	}
}

# Hot Key list
{
	"apiName": "VTubeStudioPublicAPI",
	"apiVersion": "1.0",
	"requestID": "SomeID",
	"messageType": "HotkeysInCurrentModelRequest",
	"data": {
		"modelID": "Optional_UniqueIDOfModel",
		"live2DItemFileName": "Optional_Live2DItemFileName"
	}
}

# Hot Key trriger
{
	"apiName": "VTubeStudioPublicAPI",
	"apiVersion": "1.0",
	"requestID": "SomeID",
	"messageType": "HotkeyTriggerRequest",
	"data": {
		"hotkeyID": "HotkeyNameOrUniqueIdOfHotkeyToExecute",
		"itemInstanceID": "Optional_ItemInstanceIdOfLive2DItemToTriggerThisHotkeyFor"
	}
}
"""
# %%
