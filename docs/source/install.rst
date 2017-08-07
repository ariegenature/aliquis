Installation and configuration
------------------------------

Installation
------------

XXX: TODO

Configuration
-------------

Once installation is done, you have to configure Aliquis to match your environment. Go to the
application root folder (XXX: which one), and copy the provided example configuration file
``settings.ini.example`` into a new file named ``settings.ini`` in the same folder.

.. code-block:: bash

   aliquis$ cp settings.ini.example settings.ini

Then edit ``settings.ini`` so that it suits your environment. Possible configuration parameters are
found in sections ``[aliquis]`` and ``[ldap]``. The following parameters are available in main
section ``[aliquis]`` :

* ``DEBUG``. If set to ``True``, Aliquis will print debug messages to the console. You are strongly
  advised to set this to ``False`` in production, since otherwise Aliquis will consume lot of disk
  space, will fill logs with bothering messages, and will slow down.
