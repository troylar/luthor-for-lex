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

# Cre

