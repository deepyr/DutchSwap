.. _contributing:

==================
Ways to contribute
==================

Dutch Swap is a community-driven and open source project.
There are many ways to contribute to the DutchSwap project, it's as much about the code as it is the community. Here are some way to get involved regardless of your 
skill set:

-  **Be part of the community.** The best way to contribute to DutchSwap and help
   us grow is simply to use the auctions and promote the experience by
   word-of-mouth, blog posts, tutorials,
   videos, test contracts, support on the forums, Discord. You get the point.
   Being a user and advocate helps spread the word about DutchSwap,
   which has no marketing budget and relies on its community
   for adoption.

-  **Make auctions.** It's our main focus to convince new projects and especially the
   industry at large that DutchSwap and Dutch auctions are a relevant option - We need auctions to be
   made with Dutch Swap. We know that the framework has a lot of potential and just needs usage to
   draw attention to Dutch Swap. So keep working on your awesome projects, and if you
   find a project looking for a better method of price discovery for their token - send them our way!

-  **Donate.** Dutch Swap is an open sourced project, but it can still benefit from
   user donations for many things. 
   Most importantly, we use donation money to hire core developers so they
   can work full-time on the protocol. Full-tme development has been very beneficial to the project so far and ensures a quality product on first offering.
   If you want to donate
   some tokens to the project, check `our website <https://dutchswap.com/>`_
   for details.
   
-  **Get involved in the development.** Developers of all levels can help improve DutchSwap. 
   This can be by contributing code via pull requests, testing the contracts directly on chain or on the
   git *master* branch, reporting bugs or suggesting enhancements on the issue
   tracker, improve the official documentation (both the class reference and
   tutorials) and its translations. Our development team would love to have you on board.
   The following sections will cover each of those "direct" ways
   of contributing.


Contributing code
-----------------

The possibility to study, use, modify and redistribute modifications of the
dutch swaps's source code are the fundamental rights that
Dutch Swap's `MIT <https://tldrlegal.com/license/mit-license>`_ license grants you,
making it `free and open source software <https://en.wikipedia.org/wiki/Free_and_open-source_software>`_.

As such, everyone is entitled to modify
`Dutch Swap's source code <https://github.com/deepyr/dutchswap>`_, and send those
modifications back to the upstream project in the form of a patch (a text file
describing the changes in a ready-to-apply manner) or - in the modern workflow
that we use - via a so-called "pull request" (PR), i.e. a proposal to directly
merge one or more Git commits (patches) into the main development branch.

Contributing code changes upstream has two big advantages:

-  Your own code will be reviewed and improved by other developers, and will be
   further maintained directly in the upstream project, so you won't have to
   reapply your own changes every time you move to a newer version. On the
   other hand it comes with a responsibility, as your changes have to be
   generic enough to be beneficial to all users, and not just your project; so
   in some cases it might still be relevant to keep your changes only for your
   own project, if they are too specific.

-  The whole community will benefit from your work, and other contributors will
   behave the same way, contributing code that will be beneficial to you. At
   the time of this writing, more than 1000 developers have contributed code
   changes to the engine!

To ensure good collaboration and overall quality, the Dutch Swap developers
enforce some rules for code contributions, for example regarding the style to
use in the C++ code (indentation, brackets, etc.) or the Git and PR workflow.

A good place to start is by searching for issues tagged as `junior jobs <https://github.com/deepyr/dutchswap/issues?q=is%3Aissue+is%3Aopen+label%3A%22junior+job%22>`_ (or `Hacktoberfest <https://github.com/deepyr/dutchswap/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+label%3AHacktoberfest+>`_ during October) on GitHub.

.. seealso:: Technical details about the PR workflow are outlined in a
             specific section, :ref:`doc_pr_workflow`.

             Details about the code style guidelines and the ``clang-format``
             tool used to enforce them are outlined in
             :ref:`doc_code_style_guidelines`.


Testing and reporting issues
----------------------------

Another great way of contributing to the engine is to test development releases
or the development branch and to report issues. It is also helpful to report
issues discovered in stable releases, so that they can be fixed in
the development branch and in future maintenance releases.


Testing development versions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To help with the testing, you have several possibilities:

-  Compile the engine from source yourself, following the instructions of the
   :ref:`Compiling <toc-devel-compiling>` page for your platform.

-  Test official pre-release binaries when they are announced (usually on the
   blog and other community platforms), such as alpha, beta and release candidate (RC) builds.

-  Test "trusted" unofficial builds of the development branch; just ask
   community members for reliable providers. Whenever possible, it's best to
   use official binaries or to compile yourself though, to be sure about the
   provenance of your binaries.

As mentioned previously, it is also helpful to keep your eyes peeled for
potential bugs that might still be present in the stable releases, especially
when using some niche features of the engine which might get less testing by
the developers.


Filing an issue on GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~

Dutch Swap uses `GitHub's issue tracker <https://github.com/deepyr/dutchswap/issues>`_
for bug reports and enhancement suggestions. You will need a GitHub account to
be able to open a new issue there, and click on the "New issue" button.

When you report a bug, you should keep in mind that the process is similar
to an appointment with your doctor. You noticed *symptoms* that make you think
that something might be wrong (the engine crashes, some features don't work as
expected, etc.). It's the role of the bug triaging team and the developers to
then help make the diagnosis of the issue you met, so that the actual cause of
the bug can be identified and addressed.

You should therefore always ask yourself: what is relevant information to
give so that other Dutch Swap contributors can understand the bug, identify it and
hopefully fix it. Here are some of the most important infos that you should
always provide:

-  **Operating system.** Sometimes bugs are system-specific, i.e. they happen
   only on Windows, or only on Linux, etc. That's particularly relevant for all
   bugs related to OS interfaces, such as file management, input, window
   management, audio, etc.

-  **Hardware.** Sometimes bugs are hardware-specific, i.e. they happen
   only on certain processors, graphic cards, etc. If you are able to,
   it can be helpful to include information on your hardware.

-  **Dutch Swap version.** This is a must have. Some issues might be relevant in the
   current stable release, but fixed in the development branch, or the other
   way around. You might also be using an obsolete version of Dutch Swap and
   experiencing a known issue fixed in a later version, so knowing this from
   the start helps to speed up the diagnosis.

-  **How to reproduce the bug.** In the majority of cases, bugs are
   reproducible, i.e. it is possible to trigger them reliably by following some
   steps. Please always describe those steps as clearly as possible, so that
   everyone can try to reproduce the issue and confirm it. Ideally, make a demo
   project that reproduces this issue out of the box, zip it and attach it to
   the issue (you can do this by drag and drop).
   Even if you think that the issue is trivial to reproduce, adding a minimal
   project that lets reproduce it is a big added value. You have to keep in
   mind that there are thousands of issues in the tracker, and developers can
   only dedicate little time to each issue.

When you click the "New issue" button, you should be presented with a text area
prefilled with our issue template. Please try to follow it so that all issues
are consistent and provide the required information.


Contributing to the documentation
---------------------------------

There are two separate resources referred to as "documentation" in Dutch Swap:

-  **The class reference.** This is the documentation for the complete Dutch Swap
   API as exposed to GDScript and the other scripting languages. It can be
   consulted offline, directly in Dutch Swap's code editor, or online at
   :ref:`Dutch Swap API <toc-class-ref>`.
   To contribute to the class reference, you have to edit the
   `doc/base/classes.xml` in Dutch Swap's Git repository, and make a pull request.
   See :ref:`doc_updating_the_class_reference` for more details.

-  **The tutorials and engine documentation and its translations.** This is the part you are reading
   now, which is distributed in the HTML, PDF and EPUB formats. Its contents
   are generated from plain text files in the reStructured Text (rst) format,
   to which you can contribute via pull requests on the
   `godot-docs <https://github.com/deepyr/dutchswap-docs>`_ GitHub repository.
   See :ref:`doc_documentation_guidelines` for more details.


Contributing translations
-------------------------

To make Dutch Swap accessible to everyone, including users who may prefer resources
in their native language instead of English, our community helps translate both
the Dutch Swap editor and its documentation in many languages.

See :ref:`doc_editor_and_docs_localization` for more details.
