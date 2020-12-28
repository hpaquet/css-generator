CSS-Generator
=============

What is this?
-------------

css-generator is a tool to work with css stylesheet with python. It allow you to take a an existing css stylesheet and parse it to have a css object that can be modified or to create a css file in a python script.

Install
-------

To install *CSS-Generator*, run the following command:

    pip install css-generator
	
Usage
-----


After install, to use *CSS-Generator* to create a new css file, use the following code:
	 
.. code-block:: python
	 
	from css_generator import StyleSheet
    from css_generator import Rule
    
    stylesheet = StyleSheet()
    
    container = Rule(
        rule_selector='container',
        rule_type='class',
        properties={
            'position': 'relative',
            'width': '100 %'
        }
    )
    
    stylesheet.add_rule(container)
    
    stylesheet.css(path='style.css')
	
If you want to load an existing stylesheet use:
	
.. code-block:: python
	
	from css_generator import parser

    style = parser.from_file(path='style.css')
	
	