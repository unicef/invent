from unittest import TestCase, mock
from .adapters import AzureUserManagement

class AzureUserManagementTest(TestCase):
    @mock.patch('requests.post')
    def test_get_access_token(self, mock_post):
        # Mocking successful response
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'access_token': 'test_token'}
        mock_post.return_value = mock_response
        
        azure_adapter = AzureUserManagement()

        access_token = azure_adapter.get_access_token()

        self.assertEqual(access_token, 'test_token')
        mock_post.assert_called_once_with(
            url='https://login.microsoftonline.com/test_tenant_id/oauth2/token',
            data={
                'grant_type': 'client_credentials',
                'client_id': 'test_client_id',
                'client_secret': 'test_client_secret',
                'resource': 'https://graph.microsoft.com'
            }
        )
