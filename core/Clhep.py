#!/usr/bin/env python
# Author P G Jones - 12/05/2012 <p.g.jones@qmul.ac.uk> : First revision
# The CLHEP packages base class
import LocalPackage
import os
import PackageUtil

class Clhep( LocalPackage.LocalPackage ):
    """ Base clhep installer, different versions only have different names."""
    def __init__( self, name, cachePath, installPath, tarName ):
        """ Initialise the clhep package."""
        super( Clhep, self ).__init__( name, cachePath, installPath, False )
        self._TarName = tarName
        return
    # Functions to override
    def CheckState( self ):
        """ Derived classes should override this to ascertain the package status, downloaded? installed?"""
        if os.path.exists( os.path.join( self._CachePath, self._TarName ) ):
            self._SetMode( 1 ) # Downloaded 
        if os.path.exists( os.path.join( self.GetInstallPath(), "lib/libCLHEP.a" ) ):
            self._SetMode( 2 ) # Installed as well
        return
    def GetDependencies( self ):
        """ Return the dependency names as a list of names."""
        return [ "make", "g++", "gcc" ]
    def _Install( self ):
        """ Derived classes should override this to install the package, should install only when finished. Return True on success."""
        result = PackageUtil.UnTarFile( self._TarName, self.GetInstallPath(), 2 )
        result = result && PackageUtil.ExecuteSimpleCommand( './configure', ['--prefix=%s' % self.GetInstallPath() ], None, self.GetInstallPath() )
        result = result && PackageUtil.ExecuteSimpleCommand( 'make', [], None, self.GetInstallPath() )
        result = result && PackageUtil.ExecuteSimpleCommand( 'make', ["install"], None, self.GetInstallPath() )
        return result