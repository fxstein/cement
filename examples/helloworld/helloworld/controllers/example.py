"""This is the Example controller for helloworld."""

from cement import namespaces
from cement.core.controller import CementController, expose
from cement.core.hook import run_hooks

from helloworld.model.example import ExampleModel

class ExampleController(CementController):
    """
    This is how to add a local/plugin subcommand because it will be  
    under the 'example' namespace.  You would access this subcommand as:
    
        $ myapp example ex1
        
    """
    @expose() # no template, global namespace (default)
    def ex1(self, opts, args):
        print "This is ExampleController.ex1()"
        
        # commands are all passed the opts, args from the command line.

        # Here we show how to run hooks that we've defined:
        for res in run_hooks('my_example_hook'):
            print res['sec1']
        
    def ex1_help(self, opts, args):
        print "This is the help method for ex1."
    
    @expose('helloworld.templates.example.ex2')    
    def ex2(self, opts, args): 
        """
        This is an example global command.  See --help.  When commands are
        called, they are passed the cli options and args passed after it.
        
        Notice that you can specify the namespace via the decorator parameters.
        If a plugin has any non-global commands they are grouped under a 
        single command to the base cli application.  For example, you will 
        see global commands and namespaces* when you execute:
        
            myapp --help
            
            
        If 'myplugin' has local commands, you will see 'myplugin*' show up in 
        the global commands list, and then the plugin subcommands will be seen 
        under:
        
            myapp myplugin --help
            
        
        This is done to give different options in how your application works.
        """
        
        # Here we are using our Example model, and then returning a dictionary
        # to our @expose() decorator where it will be rendered with Genshi.
        example = ExampleModel()
        example.label = 'This is my Example Model'

        # You can see if options where passed.  These are set in 
        # myapp/plugins/example.py:
        if opts.global_option:
            # --global-option was passed, do something
            print '%s passed by --global-option' % opts.global_option
            pass

        return dict(foo=True, example=example, items=['one', 'two', 'three'])

    @expose(namespace='helloworld_core')
    def ex3(self, opts, args):
        """
        This is how to add a local/plugin subcommand to another namespace.  It
        is possible to use this in conjunction with the options_hook() to add 
        additional functionality to a completely other namespace:
    
            $ myapp helloworld ex3
        
        """
        print "In helloworld_core namespace"