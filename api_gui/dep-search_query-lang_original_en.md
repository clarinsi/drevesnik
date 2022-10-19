# Query language

This page documents the search expression language which is used to query the dependency parsed corpora in the [Drevesnik](https://orodja.cjvt.si/drevesnik/en) online interface. It is based on the query language of the [dep_search](https://github.com/TurkuNLP/dep_search) tool developed by the University of Turku. In addition to querying the morphological and dependency annotations using the [Universal Dependencies](https://universaldependencies.org/) scheme, it also enables searching by the language-specific [JOS](https://nl.ijs.si/jos/) morphosyntactic tags (XPOS column in Slovenian CONLL-U treebanks).

All expression examples below are links that search through the reference SSJ dependency treebank (randomized results, short sentences).

## Token specification

### Querying by word forms

Tokens with particular word form are searched by typing the token text as-is. Examples:

*   [hodim](https://orodja.cjvt.si/drevesnik/show/en/demo1a/sl/0/10) searches for all tokens with the form _hodim_ 'I walk', written in lowercase letters
*   [Delo](https://orodja.cjvt.si/drevesnik/show/en/demo2a/sl/0/10) searches for all tokens with the form _Delo_ (newspaper name, lit. 'work'), written with the first letter capitalized

<!--- left out, as querying by values or attributes only doesn't work

If the searched text conflicts with a know morphological tag, the text is interpreted to mean the tag. To search for the actual text instead, the text must be written in quotation marks:

*   ["Person"](http://bionlp-www.utu.fi/dep_search/?db=English&search=%22Person%22) searches for literal text _Person_ and not the tag _Person_

--->

Base form (lemma) is given with the **L=** prefix:

*   [L=hoditi](https://orodja.cjvt.si/drevesnik/show/en/demo2b/sl/0/10) searches for all tokens with the lemma _hoditi_ 'to walk'

### Querying by morphological features

Part-of-speech categories and other morphological features can be defined in two ways, as all corpora are annotated both by the cross-linguistically standardized <a href="https://universaldependencies.org/" target="_blank">Universal Dependencies</a> (UD) annotation scheme and the local language-specific <a href="https://nl.ijs.si/jos/" target="_blank">JOS</a> annotation scheme. Both schemes are well documented and comparable with respect to an adequate description of Slovenian morphology, so the choice of the annotation scheme mostly depends on the user's preferences. 

#### JOS morphosyntactic tags
JOS morphosyntactic tags (XPOS column in Slovenian CONLLU treebanks) can be specified using the **X=** prefix. Given that each position in the tag represents a specific morphological feature with multiple possible values, the use of special operators is also supported, i.e. the dot operator (`.`) what matches any character and the asterisk operator (`*`) that matches 0 or more repetitions of the preceding character. Some examples:

*   [X=Ncfsl](https://orodja.cjvt.si/drevesnik/show/en/demo3a/sl/0/10) searches for all tokens with the JOS tag for feminine common nouns in locative singular
*   [X=Ncf.l](https://orodja.cjvt.si/drevesnik/show/en/demo4a/sl/0/10) searches for all tokens with the JOS tag for feminine common nouns in locative and any number
*   [X=Ncf.\*](https://orodja.cjvt.si/drevesnik/show/en/demo5a/sl/0/10) searches for all tokens with the JOS tag for feminine common nouns in any case and number

#### UD morphological features

The part-of-speech category can be specified by writing the tags as-is, while other morphological features are defined as attribute-value pairs in the form of `Category=Tag`.

*   [NOUN](https://orodja.cjvt.si/drevesnik/show/en/demo6a/sl/0/10) searches for all token with the POS tag _NOUN_ (common nouns)
*   [VerbForm=Inf](https://orodja.cjvt.si/drevesnik/show/en/demo7a/sl/0/10) searches for all tokens with the infinitive verb form

<!--- left out, as querying by values or attributes only doesn't work

*   [VerbForm=Inf](http://bionlp-www.utu.fi/dep_search/?db=Finnish&search=VerbForm%3DInf) searches for all infinitives
*   [Past](http://bionlp-www.utu.fi/dep_search/?db=Finnish&search=Past) searches for all past tense verbs (Note: _Past_ is interpreted to mean _Tense=Past_. Other possible category for _Past_ is _PartForm_, and to search for past participles _PartForm=Past_ must be typed.)

Also the whole categories can be searched. This is done by typing just the plain category name the same way than the tag values are used.

*   [PartForm](http://bionlp-www.utu.fi/dep_search/?db=Finnish&search=PartForm) searches for all participles: present (PartForm=Pres), past (PartForm=Past), agentive (PartForm=Agt) and negative (PartForm=Neg)

The full set of categories and tags used in any supported corpus can be found under the _Show types_ link on the main page (see e.g. [English](http://bionlp-www.utu.fi/dep_search/types/English) and [Czech](http://bionlp-www.utu.fi/dep_search/types/Czech)).  

--->

### Special operators
  
It is also possible to combine all above token specifications with the AND (**&**) and OR (**|**) operators:

*   [L=delati|L=narediti](https://orodja.cjvt.si/drevesnik/show/en/demo9a/sl/0/10) searches for all tokens with the lemma  _delati_ 'to do' (imperfective) or _narediti_ 'to do' (perfective)
*   [NOUN&Number=Plur](https://orodja.cjvt.si/drevesnik/show/en/demo10a/sl/0/10) searches for all nouns in plural
*   [L=prst&Gender=Masc](https://orodja.cjvt.si/drevesnik/show/en/demo11a/sl/0/10) searches for all tokens with the lemma _prst_ 'thumb' in masculine (as opposed to _prst_ 'soil' in feminine)
*   [lepo&X=R.\*](https://orodja.cjvt.si/drevesnik/show/en/demo8a/sl/0/10) searches for all tokens with the word form _lepo_ 'nice', which are marked as adverbs in JOS (and not adjectives, for example)

Word forms, lemmas and tags can also be **negated** by typing the negation operator **!** before a feature. Some examples:

*   [L=biti&!AUX](https://orodja.cjvt.si/drevesnik/show/en/demo12a/sl/0/10) searches for all tokens with the lemma _biti_ 'to be', which are not marked as an auxiliary
*   [ADJ&!X=A.\*](https://orodja.cjvt.si/drevesnik/show/en/demo13a/sl/0/10) searches for all tokens annotated as an adjective in UD, but a different part-of-speech category in JOS

Token can be left unspecified by typing an underscore character ('_').

## Dependency specification

Dependencies are expressed using `<` and `>` operators, which mimick the "arrows" in the dependency graph.

*   `A < B` means that token A is governed by token B, e.g. _rainy_ < _morning_
*   `A > B` means that token A governs token B, e.g. _read_ > _newspapers_

The underscore character `_` stands for _any token_, that is, a token on which we place no particular restrictions. Here are simple examples of basic search expressions that restrict dependency structures:


*   [delo < \_](https://orodja.cjvt.si/drevesnik/show/en/demo14a/sl/0/10) searches for all cases of _delo_ 'work' which are governed by some word
*   [delo > \_](https://orodja.cjvt.si/drevesnik/show/en/demo15a/sl/0/10) searches for all cases of _delo_  which govern a word
*   [\_ < delo](https://orodja.cjvt.si/drevesnik/show/en/demo16a/sl/0/10) searches for any token governed by _delo_ 

Note that the left-most token in the expression is always the target of the search and also identified in search results (marked as green). While queries `delo > _` and `_ < delo` return the excact same graphs, matched tokens differ.

The **dependency type** can be specified typing it right after the dependency operator, e.g. `_ <type _` or `_ >type _`. The `|` character denotes a logical _or_, so any of the given dependency relations will match.

*   [\_ <cop \_](https://orodja.cjvt.si/drevesnik/show/en/demo17a/sl/0/10) searches for all copula verbs (i.e. tokens which are governed through a _cop_ dependency)
*   [\_ >nsubj \_](https://orodja.cjvt.si/drevesnik/show/en/demo18a/sl/0/10) searches for all words governing a nominal subject (i.e. various kinds of predicates)
*   [\_ <nsubj|<csubj \_](https://orodja.cjvt.si/drevesnik/show/en/demo19a/sl/0/10) searches for all words serving as a subject - either as a nominal or clausal subject

You can specify a number of dependency restrictions at a time by chaining the operators:


*   [\_ >obj \_ >iobj \_](https://orodja.cjvt.si/drevesnik/show/en/demo20a/sl/0/10) searches for words that govern both direct and indirect objects (e.g. ditransitive predicates)
*   [\_ <amod \_ >advmod \_](https://orodja.cjvt.si/drevesnik/show/en/demo21a/sl/0/10) searches for words that serve as adjectival modifiers and at the same time govern an adverbial modifier
*   [\_ >nmod \_ >nmod \_](https://orodja.cjvt.si/drevesnik/show/en/demo22a/sl/0/10) earches for words that govern two distinct nominal modifiers

Priority is marked using parentheses:

*   [\_ >nmod \_ >nmod \_](https://orodja.cjvt.si/drevesnik/show/en/demo23a/sl/0/10) searches for words that govern two distinct nominal modifiers (two nommod dependencies in parallel)
*   [\_ >nmod (\_ >nmod \_)](https://orodja.cjvt.si/drevesnik/show/en/demo24a/sl/0/10) searches for words that govern a nominal modifier which, in turn governs another nominal modifier (chain of two nmod dependencies)


**Negation** is marked using the negation operator `!`, which can be used to negate the `<` and `>` operators as well as specific dependency types. Some examples:

*   [\_ >nmod \_ !>case \_](https://orodja.cjvt.si/drevesnik/show/en/demo25a/sl/0/10) searches for all nominal modifiers that do not govern a case marker (i.e. nominal modifiers that are not prepositional phrases)
*   [\_ >nmod \_ >!case \_](https://orodja.cjvt.si/drevesnik/show/en/demo26a/sl/0/10) searches for all nominal modifiers that govern some word, but not a case marker

<!--- ta kombinacija ne dela kot pričakovano - vrne tudi advcl z mark ... najbrž manjka 'for every dependent'
*   [\_ <advcl \_ !>mark \_](http://bionlp-www.utu.fi/dep_search/?db=English&search=_%20%3Cadvcl%20_%20%21%3Emark%20_) searches for heads of unmarked adverbial clauses (governed by advcl but not governing mark)
*   [\_ <nsubj \_ !(>amod|>acl) \_](http://bionlp-www.utu.fi/dep_search/?db=English&search=_%20%3Cnsubj%20_%20%21%28%3Eamod%7C%3Eacl%29%20_) searches for subjects which do not govern adjectival or participial modifiers
*   [\_ <nsubj \_ >!amod \_](http://bionlp-www.utu.fi/dep_search/?db=English&search=_%20%3Cnsubj%20_%20%3E%21amod%20_) searches for subjects which governs something but it cannot be an adjective (governed by nsubj and governs something which is not amod)
--->
*   [\_ <nsubj \_ !(>amod|>acl) \_](https://orodja.cjvt.si/drevesnik/show/en/demo27a/sl/0/10) searches for nominal subjects which do not govern adjectival or participial modifiers
*   
Note that negating a relation (e.g. `_ !>amod _`) allows for the token not having any dependent, whereas negating a type (e.g. `_ >!amod _`) means that the token must have at least one dependent (which is not _amod_).

**Direction** of the dependency relation can be specified using operators `@R` and `@L`, where the operator means that the right-most token of the expression must be at the right side or at the left side, respectively.

*   [VERB >nsubj@R \_](https://orodja.cjvt.si/drevesnik/show/en/demo28a/sl/0/10) searches for verbs which have _nsubj_ dependent to the right
*   [\_ >amod@L \_ >amod@R \_](https://orodja.cjvt.si/drevesnik/show/en/demo29a/sl/0/10) searches for words that have two distinct adjectival modifiers (two _amod_ dependencies in parallel), one must be at the left side, the other at the right side
*   [\_ <case@L \_](https://orodja.cjvt.si/drevesnik/show/en/demo30a/sl/0/10) searches for case markers where the governor token is at the left side, i.e. postpositions (as compared to prepositions)

## Combining queries

Several queries can be combined with the `+` operator. A query of the form query1 + query2 + query3 returns all trees which independently satisfy all three queries.

*   [VERB >aux \_ + Tense=Pres](https://orodja.cjvt.si/drevesnik/show/en/demo31a/sl/0/10) searches for trees with a simple and a complex verb phrase

## Universal quantifcation

The operator '->' introduces a condition that all the matched tokens should fulfill (i.e. the tokens or structures preceding this operator). For example:

*   [\_ -> NOUN](https://orodja.cjvt.si/drevesnik/show/en/demo32a/sl/0/10) means "every token (`_`) must be a NOUN" and thus matches sentences with nouns only
*   [NOUN -> NOUN >amod \_](https://orodja.cjvt.si/drevesnik/show/en/demo33a/sl/0/10) means "all nouns must govern an adjectival modifier" and thus matches sentences with modified nouns only 
