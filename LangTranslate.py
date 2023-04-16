from textblob import TextBlob
from RapidAPI import RapidAPIAPIWrapper
import click


def translate(input, source, target, rapidapi_wrapper):
    # Prepare the RapidAPIAPIWrapper
    rapidapi_wrapper.config["apiKey"] = "APIKEY"
    rapidapi_wrapper.config["host"] = "HOSTURL"
    
    # Update the run method in RapidAPIAPIWrapper
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

    # Update the _get_headers method in RapidAPIAPIWrapper
    def _get_headers(self):
        headers = {
            "x-rapidapi-key": self.config["apiKey"],
            "x-rapidapi-host": self.config["host"]
        }
        return headers

    # Update the _get_params method in RapidAPIAPIWrapper
    def _get_params(self, query, source, target):
        params = {
            "q": query,
            "source": source,
            "target": target
        }
        return params
    
    # Update the _get_base_url method in RapidAPIAPIWrapper
    def _get_base_url(self):
        return f"https://{self.config['host']}/language/translate/v2"

    # Perform the translation
    query = input
    response = rapidapi_wrapper.run(source, target, input)
    
    translated_text = response['data']['translations'][0]['translatedText']

    return translated_text



@click.command()
@click.option('--input', prompt='Enter input text', help='Input text to translate')
@click.option('--source', prompt='Enter source language code', help='Source language code')
@click.option('--target', prompt='Enter target language code', help='Target language code')
@click.option('--output', prompt='Enter output format', help='Output format')
@click.option('--save', prompt='Save to file? (y/n)', help='Save result to file?')
def process(input, source, target, output, save):
    rapidapi_key = "9ab76486aemsh6ff069083262441p1a2936jsn35f34234c26b"
    rapidapi_host = "google-translate1.p.rapidapi.com"
    rapidapi_wrapper = RapidAPIAPIWrapper(rapidapi_key, rapidapi_host)

    try:
        translated_text = translate(input, source, target, rapidapi_wrapper)
        polarity, subjectivity = analyze_sentiment(translated_text)

        click.echo(f'Sentiment Polarity: {polarity}')
        click.echo(f'Sentiment Subjectivity: {subjectivity}')

        if save.lower() == 'y':
            save_to_file(translated_text, output)

        click.echo(translated_text)

    except Exception as e:
        click.echo(f'Error: {str(e)}')


def analyze_sentiment(translated_text):
    try:
        blob = TextBlob(translated_text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        return polarity, subjectivity

    except Exception as e:
        click.echo(f'Error: {str(e)}')


def save_to_file(translated_text, output_file):
    try:
        with open(output_file, 'w') as file:
            file.write(translated_text)

    except Exception as e:
        click.echo(f'Error: {str(e)}')


if __name__ == '__main__':
    process()
