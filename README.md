# nalgene

A natural language generation language, intended for creating training data for intent parsing systems.

## Overview

Nalgene generates pairs of sentences and grammar trees by a random (or guided) walk through a grammar file.

* Sentence: the natural language sentence, e.g. "turn on the light"
* Tree: a nested list of tokens ([an s-expression](https://en.wikipedia.org/wiki/S-expression)) generated alongside the sentence, e.g.

	```
    ( %setDeviceState
        ( $device.name light )
        ( $device.state on ) ) )
	```

## Usage

```
$ python gui.py 
```
Add the desired input in the first input box in the form of a dictionary, e.g.:

* {"proposition": "subject", "subject": "hund", "action": "nehmen", "activation": 1.40}

For the system to work correctly the proposition, name of the entity and activation is mandatory.
The proposed propositions currently are subject, entity, property, part_of, relpos and direction.
Additionally, subjects need an action specified with one possible object (entity) and an infostate (new / old). 
Other entities, who will be the indirect objects of the sentence, need to have a function (location / modality) are the
current possibilities. The direct object does not need a function. Relpos / part_of relation need the value rel_entity
specifying the relative entity. Relations and properties also need the value attribute.

To add entries into the lexicon, use the second input line.
Current classes are Subject, Entity, Action and Attribute.

* Subjects are represented like this: Subject('m', 'hund', known=True)
where m represents the genus, 'hund' represents the value and known (default = False) represents if the word is known to the system. 

* Actions are specified like this: Action("nehmen","genommen", known=True), where genommen represents the present 
perfect tense

* Attributes are specified like this: Attribute("laffe", "rund", known=True), where laffe represents the entity which
is specified by the attribute. It is important that attributes are added only after the entity is added 
(see order in the list, entities must be above attributes)!

## Syntax

A .nlg nalgene grammar file is a set of sections separated by a blank line. Every section takes this shape:

```
node_name
    token sequence 1
    token sequence 2
```

The indented lines under a node are the node's possible token sequences. Each token in a sequence is either

* a regular word (no prefix),
* a `%phrase` node,
* a `$value` node,
* a `@ref` node,
* or a `~synonym` word.

Each token is added to the output sentence and/or tree during generation, depending on the type.

A standard .nlg file starts with a *start phrase* `%`, which is the default entry point for the generator. The generator may also use a specific entry point.

## Phrases

A phrase (`%phrase`) is a general set of token sequences. A phrase is potentially recursive, using tokens which represent other phrases (even itself). Each phrase defines one or more possible sequences.

The regular words in a phrase are ignored in the output tree. This makes them useful for defining higher level grammar for the same intent - for example, for different word orders ("turn on the light" vs "turn the light on").

Using this grammar:

```
%
    %greeting
    %farewell
    %greeting and %farewell

%greeting
    hey there
    hi

%farewell
    goodbye
    bye
```

The generator might output:

```
> hey there and bye
( %
    ( %greeting )
    ( %farewell ) )
```

#### Basic generation walkthrough

Here's how the generator arrived at this specific sentence and tree pair:

* Start at start node `%`, with an empty output sentence `""` and tree `( % )`
* Randomly choose a token sequence, in this case the 3rd: `%greeting and %farewell`
* The first token is a phrase token `%greeting`, so
    * Add a new sub-tree `( %greeting )` to the parent tree
    * Look up the token sequences for `%greeting`
    * Choose one, in this case `hey there`
        * For both of these regular word tokens, add to the output sentence (but not to the tree)
* At this point the output sentence is `"hey there"` and the parse tree is `( % ( %greeting ) )`
* The second token is a regular word `"and"`, so add it to the output sentence
* The third token is another phrase `%farewell`, so
    * Add a new sub-tree `( %farewell )` to the parent tree
    * Look up the token sequences for `%farewell`
    * Choose one, in this case `bye`
        * Add to the output sentence
        * Now the output sentence is `"hey there and bye"`
* No more tokens, so we're done

## Values

Sometimes you need to capture the specific words in a sentence, for example to capture the location in a sentence like "how is the weather in boston". Values, marked with a dollar sign as `$value`, are a type of leaf node that capture the regular word tokens in the tree.

```
%getWeather
    what is the weather in $location
    how is the $location weather

$location
    boston
    san francisco
    tokyo
```

```
> what is the weather in san francisco
( %getWeather
    ( $location san francisco ) )
```

## Refs

**TODO**: Better name for this

As an alternative to the freeform `$value`, there is a `@ref` leaf node which references a specific value without capturing the words beneath it. This allows you to reference a specific entity, e.g. a specific room or device name, with multiple expansions.

```
%turnOnLight
    turn the %light on

%light
    @office_light
    @living_room_light

@office_light
    office light
    light in the office

@living
    light in the den
    light in the living room
    living room light
```

## Synonyms

Synonyms, marked `~synonym`, are output only on the sentence side, and are useful for supplying word variations.

```
%good
    ~exclamation this is ~so ~good

~exclamation
    wow
    omg

~so
    so
    very
    extremely

~good
    good
    great
    wonderful
```

```
> wow this is extremely great
( %good )
```

## Optional tokens

Tokens with a `?` at the end will be used only 50% of the time.

```
%findFood
    ~find $price? $food ~near $location
```

```
> find me sushi in san francisco
( %
    ( %findFood
        ( $food sushi )
        ( $location san francisco ) ) )

> tell me the cheap fried chicken around tokyo
( %
    ( %findFood
        ( $price cheap )
        ( $food fried chicken )
        ( $location tokyo ) ) )
```

## Passthrough tokens

Tokens with a `=` at the end are called "passthrough" tokens and will not be included in the output tree, but their children will be. This is defined at the root level, rather than within a token sequence.

```
%
    ~please? %command

%command=
    %getTime
    %getFact

%getTime
    what time is it
    what is the time

%getFact=
    %getLocationFact
    %getPersonFact
    %getPersonalFact
```

In this case, whenever the `%command` token is encountered, whatever its children output will be directly added to the tree (as opposed to prefixed with the `%command` token), so it will be output as `%getTime` or `%getFact`. But in fact `%getFact` is another passthrough token, so the value of its children will be passed all the way up the tree.

```
> what is the time
( %
    ( %getTime ) )

> pretty please what is the population of tokyo
( %
    ( %getLocationFact
        ( $location_fact population )
        ( $location tokyo ) ) )
```

