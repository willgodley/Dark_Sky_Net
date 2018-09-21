ADD:
- Will Godley
- wmgodley
- 5416-2656
- Instructions on how to run your submission
  > Download the files and place them in a directory. Navigate to that directory
  in terminal and run the program on the terminal command line using:
  $ python3 chatbot.py

- Anything else that we need to know to grade your submission

  > When running, the following errors are caused by:
    - "Make sure you are connected to the internet"
      > Computer is not connected to the internet

    - "Is {city} a city?"
      > A non-real city has been requested ex. fhdslkahasfq

    - "Sorry, I don't know"
      > Dark Sky Net is failing

  > Example interactions:

    > Hi, my name is Will
    Hi Will. Are you a man or a woman?

    > What's the weather like in North Kingstown?
    In North Kingstown, it is 44.27 and Clear

    > Is it going to rain in Providence today?
    It almost definitely will not rain in Providence

    > How hot will it get in Narragansett today?
    In Narragansett, it will reach 46.1 degrees Fahrenheit today

    > How cold will it get in Warwick today?
    In Warwick, the low will be 32.53 degrees Fahrenheit today

    > Is it going to rain in Cranston this week?
    It will almost definitely rain in ECranston this week

    > How hot will it get in South Kingstown this week?
    In South Kingstown, it will reach 46.08 degrees Fahrenheit this week

    > How cold will it get in Barrington this week?
    In Barrington, the low will be 12.37 degrees Fahrenheit this week

    > How cold will it get in dfskjahsdkjfhasldkjfh this week?
    Is dfskjahsdkjfhasldkjfh a city?

    > quit

    ** the program is now terminated **
    (^not program output^)

  > I have two cache files, latLongCache.json and weatherCache.json. Both
  Caches allow the program to access requested information if it has already
  been called from an API. The latLongCache stores the google information
  indefinitely, while the weatherChache will force the program to make another
  API call if the API for the specified location has not been called in the
  past 5 minutes.

  > The spec wasn't clear on how you were supposed to calculate the probability of
  rain in a day. I just took the probability of rain on the first day of the
  week from the weekly forecast data. I then used the same number cutoffs as the
  weekly probability that was given on the spec.
