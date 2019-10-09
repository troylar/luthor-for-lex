# Luthor for Amazon Lex - Multi-Bot Manager and Player

# Overview
Typically, the goal of a Lex conversation is to fulfill a single set of intents, however, there are use cases where a conversation may need to temporarily change topics.

For example, in the case of someone with special needs, a person may be in the middle of a Lex conversation ordering their lunch through the `LunchBot`, and then suddenly ask a completely irrelevant question which maybe handled by the `CommonQuestionBot`. `Luthor for Lex` can switch contexts to the question bot, and then naturally transition back to the original bot. This provides a "[stream of consciousness](https://en.wikipedia.org/wiki/Stream_of_consciousness "stream of consciousness")" flow to the conversation. 

`Luthor for Lex` allows you to run multiple simultaneous bots, switching contexts and managing the transition between bots cleanly and naturally.

# Features
* Create/update bots, slots and intents using YAML (transparently handles checksums)
* Run multiple bots at the same time within a single conversation
* Event hook model for each bot provides several points of customization
* Customizable transitions between bots to provide a natural conversation flow
* Built-in bot player, using audio or keyboard entry

 #Installation

```
$ pip install luthor-for-lex
```

# Feature #1: Bot Management
To manage bots, you can look at the `examples` folder to see the format. Basically, it the Lex schema in yaml. You separately deploy slots, intents and bots. All three use the same format:

If the item doesn't exist, it will create it. If there are changes, then it will automatically update the current entity in Lex.

```
$ luthor bot/intent/slot apply {folder containing yaml}
```

## Deploying Slots

```
$ luthor slot apply ./example/slots
```

## Deploying Intents

```
$ luthor intent apply ./example/intents
```

## Deploying Bots

```
$ luthor intent apply ./example/bots
```

# Feature #2: Bot Player
If you want to test our your bot from the command-line, `luthor` will let you interact with your bot either via audio or keyboard.

Suppose you have a bot named `SetAlarmBot` with an utterance `Set my alarm.`

```
$ luthor play SetAlarmBot --ice_breaker "Set my alarm." --required_bots SetAlarmBot --no_audio
```

The `ice_breaker` is the utterance that initates the bot. This will allow you to interact with the bot via keyboard for testing.

# Feature #3: Multiple Bots
Using multiple bots allows you to pass in multiple bots to the player and interact with multiple utterances across all of the bots. This lets you modularize your bots.

## Step 1: Create and deploy your bot
Create the yaml and deploy your complete bot.

## Step 2: Create the bots folder
If it doesn't exist, create a `./lex/bots` folder.

## Step 3: Create a bot class
Create a new file in the `./lex/bots` folder called `{botname}.py` inheriting from `BaseBot`.

For example, if you bot is called `OrderPizza`, then create a file called `./lex/bots/OrderPizza.py`:

```
class OrderPizza(BaseBot):
     def __init__(self, lexbot):
         self.bot_name = 'PizzaBot'
         self.lexbot = lexbot
         super().__init__()
```
=======

 #Installation

```
$ pip install luthor-for-lex
```

# Feature #1: Bot Management
To manage bots, you can look at the `examples` folder to see the format. Basically, it the Lex schema in yaml. You separately deploy slots, intents and bots. All three use the same format:

If the item doesn't exist, it will create it. If there are changes, then it will automatically update the current entity in Lex.

```
$ luthor bot/intent/slot apply {folder containing yaml}
```

## Deploying Slots

```
$ luthor slot apply ./example/slots
```

## Deploying Intents

```
$ luthor intent apply ./example/intents
```

## Deploying Bots

```
$ luthor bot apply ./example/bots
```

# Feature #2: Bot Player
If you want to test out your bot from the command-line, `luthor` will let you interact with your bot either via audio or keyboard.

Suppose you have a bot named `SetAlarmBot` with an utterance `Set my alarm.`

```
$ luthor play SetAlarmBot --ice_breaker "Set my alarm." --required_bots SetAlarmBot --no_audio
```

The `ice_breaker` is the utterance that initates the bot. This will allow you to interact with the bot via keyboard for testing.
