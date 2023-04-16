import requests


class BaseTool:
    def __init__(self):
        pass


    def __init__(self, api_key, host):
        self.config = {
            "apiKey": api_key,
            "host": host
        }


    def run(self, query, source, target):
        headers = self._get_headers()
        params = self._get_params(query, source, target)
        url = self._get_base_url()
        method = self._get_method()

        try:
            response = requests.request(method, url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as error:
            return self._handle_error(error)

    def _get_headers(self):
        headers = {
            "x-rapidapi-key": self.config["apiKey"],
            "x-rapidapi-host": self.config["host"]
        }
        return headers

    def _get_params(self, query, source, target):
        params = {
            "q": query,
            "source": source,
            "target": target
        }
        return params

    def _get_base_url(self):
        return f"https://{self.config['host']}/language/translate/v2"

    def _get_method(self):
        return "GET"

    def _handle_error(self, error):
        return str(error)

class RapidAPIAPIWrapper:
    def __init__(self, api_key, host):
        self.config = {
            "apiKey": api_key,
            "host": host
        }

    def run(self, source, target, text):
        headers = self._get_headers()
        data = self._get_data(source, target, text)
        url = self._get_base_url()
        method = self._get_method()

        try:
            response = requests.request(method, url, headers=headers, data=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as error:
            return self._handle_error(error)

    def _get_headers(self):
        headers = {
            "x-rapidapi-key": self.config["apiKey"],
            "x-rapidapi-host": self.config["host"],
            "content-type": "application/x-www-form-urlencoded"
        }
        return headers

    def _get_data(self, source, target, text):
        data = {
            "q": text,
            "source": source,
            "target": target
        }
        return data

    def _get_base_url(self):
        return f"https://{self.config['host']}/language/translate/v2"

    def _get_method(self):
        return "POST"

    def _handle_error(self, error):
        return str(error)


class RapidAPIToLangChainConverter(BaseTool):
    def __init__(self, api_wrapper):
        super().__init__()
        self.api_wrapper = api_wrapper

    def generate_code(self, api_endpoint):
        response = self.api_wrapper.run(api_endpoint)

        # TODO: Implement LangChain code generation based on response

        return "LangChain code"


if __name__ == "__main__":
    rapidapi_key = "apikey"
    rapidapi_host = "hosturl"
    rapidapi_wrapper = RapidAPIAPIWrapper(rapidapi_key, rapidapi_host)
    rapidapi_to_langchain_converter = RapidAPIToLangChainConverter(rapidapi_wrapper)
    api_endpoint = "apiendpoint"
    print(rapidapi_to_langchain_converter.generate_code(api_endpoint))
