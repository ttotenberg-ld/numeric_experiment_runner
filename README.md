# LaunchDarkly Numeric Experiment Runner

## WARNING
This is a utility that has the potential to spoof a LOT of data, and send real `track()` events to your LaunchDarkly account. If you are a LaunchDarkly customer stumbling on this, please use with care to avoid accidentally going over your contractual usage agreement.

This utility is unsupported, and not intended as a model for any sort of serious usage. It's a hacked together tool that solves a problem I had, nothing more. :)

## Installation
1. On the releases page, download 'ExperimentRunner.zip'. Extract 'ExperimentRunner.app' from that zip file.
1. Copy ExperimentRunner.app to your Applications folder
1. Run it!
1. The first time you do run it, MacOS will likely warn you that it's trying to save files in `/Users/[USER]/Documents/ExperimentRunner`. Click OK to allow this.

## Usage
1. Input the following information
    1. SDK Key: Your LaunchDarkly SDK key
        1. `sdk-12345-abcde`
    1. API Key: Your LaunchDarkly API key. Needs at least reader permissions.
        1. `api-12345-abcde`
    1. Project Key: Your LaunchDarkly Project key.
        1. `example-project`
    1. Flag Key: Your LaunchDarkly flag key, as it appears in code. Must be actively recording an experiment.
        1. `example-flag`
    1. Metric Key: The LaunchDarkly metric you're going to use to send `track()` events. Must be used on an actively recording experiment.
        1. `example-metric`
    1. Events: The total number of `track()` events to send to LaunchDarkly. Will be divided among your targeted variations, based on your experiment population allocation. Must be an integer.
        1. `1000`
1. Click **'Get Variations'**, which will make an API call to LaunchDarkly and populate the available variations for the Flag you entered.
1. You are presented with a list of available variations, which each have two values to input: `Center` and `Spread`.
    1. **Center:** The eventual mean of your numeric experiment values.
    1. **Spread:** The standard deviation above and below your Center.
    1. Example: I'm simulating data for an experiment on `page-load-time`, in milliseconds. My center for a variation is `70`, with a spread of `30`. That will create a normal distribution of page load time values with the majority of values between `40` and `100`, with some outliers above and below that range.
1. Click **'Preview'** to see a rough mockup of the data.
    1. ***NOTE:*** This is not the exact data that will be sent to LaunchDarkly, just a rough model based on the values you input. You can click 'Preview' multiple times, and it will generate new data and display it.
    1. Also note that the higher your `Events` value, the smoother the curve will be.
1. When ready, click **'Run Experiments'** to send the `track()` calls to LaunchDarkly.
    1. ***Clicking 'Run Experiments' will create fake users, evaluate your flag, and send real events to your LaunchDarkly account.***

## Development
Ignore this section if you just want to use the experiment runner - see Installation above instead.

To make changes to the code:
1. Install required libraries:
    1. Run `pip install -r requirements.txt`
1. Run `python main.py`

To build a package:
1. Use [PyInstaller](https://pyinstaller.org/en/stable/).
