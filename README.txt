CPSDocument
===========

$Id$

This provides a Flexible Document for CMF (it is independant of CPS). It
is based on the framework of CPSSchemas which gives us all the fields,
widget and validation we need.

This package adds a new FlexibleTypeInformation with which documents
that automatically obey a schema and some layouts can be created. It
also provides a mixin for documents who can have their schemas and
layouts inferred from a FlexibleTypeInformation or directly found in the
instance, which gives us the "flexible" part.
