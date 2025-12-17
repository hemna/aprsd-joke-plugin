import logging
import textwrap

import requests
from aprsd import packets, plugin
from aprsd.utils import trace
from oslo_config import cfg

import aprsd_joke_plugin
from aprsd_joke_plugin import conf  # noqa

CONF = cfg.CONF
LOG = logging.getLogger("APRSD")


class JokeAPIPlugin(plugin.APRSDRegexCommandPluginBase):
    """Plugin that makes use of v2.jokeapi.dev to get a joke.

    You can find the API documentation here: https://v2.jokeapi.dev/

    By default this will get a random joke in English from any category.

    The languages supported are:
    de - German
    en - English
    es - Spanish
    fr - French
    pt - Portuguese

    You can ask for a specific language by passing in
    l=<language>

    You can ask for a specific category by passing in
    c=<category>

    The categories supported are:
    Any - Any category
    Misc - Miscellaneous
    Programming - Programming jokes
    Dark - Dark jokes
    Pun - Pun jokes
    Spooky - Spooky jokes
    """

    version = aprsd_joke_plugin.__version__
    # Change this regex to match for your plugin's command
    # Tutorial on regex here: https://regexone.com/
    # Look for any command that starts with w or W
    command_regex = "^[jJ]"
    # the command is for ?
    # Change this value to a 1 word description of the plugin
    # this string is used for help
    command_name = "joke"

    enabled = False

    allowed_languages = ["de", "en", "es", "fr", "pt"]
    allowed_categories = ["Any", "Misc", "Programming", "Dark", "Pun", "Spooky"]
    category_mapping = {
        "any": "Any",
        "misc": "Misc",
        "prog": "Programming",
        "dark": "Dark",
        "pun": "Pun",
        "sp": "Spooky",
    }

    def setup(self):
        """Allows the plugin to do some 'setup' type checks in here.

        If the setup checks fail, set the self.enabled = False.  This
        will prevent the plugin from being called when packets are
        received."""
        # Do some checks here?
        self.enabled = True

    def create_threads(self):
        """This allows you to create and return a custom APRSDThread object.

        Create a child of the aprsd.threads.APRSDThread object and return it
        It will automatically get started.

        You can see an example of one here:
        https://github.com/craigerl/aprsd/blob/master/aprsd/threads.py#L141
        """
        if self.enabled:
            # You can create a background APRSDThread object here
            # Just return it for example:
            # https://github.com/hemna/aprsd-weewx-plugin/blob/master/aprsd_weewx_plugin/aprsd_weewx_plugin.py#L42-L50
            #
            return []

    def get_joke(self, language: str, category: str) -> str:
        """Get a joke from the joke API."""
        url = f"https://v2.jokeapi.dev/joke/{category}?lang={language}&blacklistFlags=explicit"
        response = requests.get(url)
        return response.json()

    @trace.trace
    def process(self, packet: packets.core.Packet):
        """This is called when a received packet matches self.command_regex.

        This is only called when self.enabled = True and the command_regex
        matches in the contents of the packet["message_text"]."""

        LOG.info("JokeAPIPlugin Plugin")
        message = packet.message_text

        # Parse the message for the language and category
        language = "en"
        category = "any"

        for word in message.split():
            if word.startswith("l="):
                language = word[2:].lower()
            elif word.startswith("c="):
                category = word[2:].lower()

        LOG.debug(f"Language: {language}")
        LOG.debug(f"Category: {category}")

        # Now valdate the language and category are in the allowed lists
        # the values passed in should be case insensitive
        if language not in self.allowed_languages:
            language = "en"
            return f"Invalid language. Use one of: {', '.join(self.allowed_languages)}"
        if category not in self.category_mapping.keys():
            category = "Any"
            return f"Invalid category. Use one of: {', '.join(self.category_mapping.keys())}"
        else:
            category = self.category_mapping[category]

        #
        # Get the joke
        joke = None
        try:
            joke = self.get_joke(language, category)
        except Exception as e:
            LOG.error(f"Error getting joke: {e}")
            return "Error getting joke"

        if joke:
            LOG.info(f"Joke: {joke}")
            if joke["type"] == "single":
                return textwrap.wrap(joke["joke"], 67, break_long_words=False)
            elif joke["type"] == "twopart":
                #
                setup = textwrap.wrap(joke["setup"], 67, break_long_words=False)
                delivery = textwrap.wrap(joke["delivery"], 67, break_long_words=False)
                LOG.debug(f"Setup: {setup}")
                LOG.debug(f"Delivery: {delivery}")
                # combine the 2 lists into a single list
                combined = setup + delivery
                return combined
            else:
                return "Unknown joke type"

        # Now we can process
        return "some reply message"
