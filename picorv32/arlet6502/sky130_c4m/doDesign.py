#!/usr/bin/env python3

import sys
import os
import traceback
import CRL
import helpers
helpers.loadUserSettings()
from   helpers.io import ErrorMessage, WarningMessage
from   helpers    import trace, l, u, n
import plugins
from   Hurricane  import DbU, Breakpoint
from   plugins.alpha.block.block         import Block
from   plugins.alpha.block.configuration import IoPin, GaugeConf
from   plugins.alpha.block.spares        import Spares
from   plugins.alpha.chip.configuration  import ChipConf
from   plugins.alpha.chip.chip           import Chip
from   plugins.alpha.core2chip.sky130    import CoreToChip


af = CRL.AllianceFramework.get()


def scriptMain ( **kw ):
    """The mandatory function to be called by Coriolis CGT/Unicorn."""
    global af
    rvalue = True
    try:
       #helpers.setTraceLevel( 540 )
       #Breakpoint.setStopLevel( 100 )
        if 'CHECK_TOOLKIT' in os.environ:
            print( 'CHECK_TOOLKIT process\n\n\n\n\n\n\n\n' )
            checkToolkitDir   = os.environ[ 'CHECK_TOOLKIT' ]
            harnessProjectDir = checkToolkitDir + '/cells/sky130'
        else:
            print( '[ERROR] The "CHECK_TOOLKIT" environment variable has not been set.'  )
            print( '        Please check "./mk/users.d/user-CONFIG.mk".'  )
            sys.exit( 1 )
        buildChip = False
        cell, editor = plugins.kwParseMain( **kw )
        cellName = 'arlet6502'
        if buildChip:
            cellName += '_harness'
        cell = af.getCell( 'arlet6502', CRL.Catalog.State.Logical )
        if editor:
            editor.setCell( cell ) 
            editor.setDbuMode( DbU.StringModePhysical )
        if buildChip:
            ioPinsSpec = [ ]
            ioPadsSpec = [ (None, None, 'power_0'  , 'vccd1'      , 'vdd'    )
                         , (None, None, 'ground_0' , 'vssd1'      , 'vss'    )
                         , (None, None, None       , 'io_in(37)'  , 'clk'    )
                         , (None, None, None       , 'io_in(0)'   , 'di(0)'  )
                         , (None, None, None       , 'io_in(1)'   , 'di(1)'  )
                         , (None, None, None       , 'io_in(2)'   , 'di(2)'  )
                         , (None, None, None       , 'io_in(3)'   , 'di(3)'  )
                         , (None, None, None       , 'io_in(4)'   , 'di(4)'  )
                         , (None, None, None       , 'io_in(5)'   , 'di(5)'  )
                         , (None, None, None       , 'io_in(6)'   , 'di(6)'  )
                         , (None, None, None       , 'io_in(7)'   , 'di(7)'  )
            
                         , (None, None, None       , 'io_out(8)'  , 'do(0)'  )
                         , (None, None, None       , 'io_out(9)'  , 'do(1)'  )
                         , (None, None, None       , 'io_out(10)' , 'do(2)'  )
                         , (None, None, None       , 'io_out(11)' , 'do(3)'  )
                         , (None, None, None       , 'io_out(12)' , 'do(4)'  )
                         , (None, None, None       , 'io_out(13)' , 'do(5)'  )
                         , (None, None, None       , 'io_out(14)' , 'do(6)'  )
                         , (None, None, None       , 'io_out(15)' , 'do(7)'  )
            
                         , (None, None, None       , 'io_in(16)'  , 'a(0)'   )
                         , (None, None, None       , 'io_in(17)'  , 'a(1)'   )
                         , (None, None, None       , 'io_in(18)'  , 'a(2)'   )
                         , (None, None, None       , 'io_in(19)'  , 'a(3)'   )
                         , (None, None, None       , 'io_in(20)'  , 'a(4)'   )
                         , (None, None, None       , 'io_in(21)'  , 'a(5)'   )
                         , (None, None, None       , 'io_in(22)'  , 'a(6)'   )
                         , (None, None, None       , 'io_in(23)'  , 'a(7)'   )
                         , (None, None, None       , 'io_in(24)'  , 'a(8)'   )
                         , (None, None, None       , 'io_in(25)'  , 'a(9)'   )
                         , (None, None, None       , 'io_in(26)'  , 'a(10)'  )
                         , (None, None, None       , 'io_in(27)'  , 'a(11)'  )
                         , (None, None, None       , 'io_in(28)'  , 'a(12)'  )
                         , (None, None, None       , 'io_in(29)'  , 'a(13)'  )
                         , (None, None, None       , 'io_in(30)'  , 'a(14)'  )
                         , (None, None, None       , 'io_in(31)'  , 'a(15)'  )
            
                         , (None, None, None       , 'io_in(32)'  , 'irq'    )
                         , (None, None, None       , 'io_in(33)'  , 'nmi'    )
                         , (None, None, None       , 'io_in(34)'  , 'rdy'    )
                         , (None, None, None       , 'io_in(35)'  , 'reset'  )
                         , (None, None, None       , 'io_in(36)'  , 'we'     )
                         ]
        else:
            m1pitch    = u(0.46)
            m2pitch    = u(0.51)
            ioPadsSpec = [ ]
            ioPinsSpec = [ (IoPin.WEST |IoPin.A_BEGIN, 'di({})'  , 10*m1pitch, 10*m1pitch,  8)
                         , (IoPin.WEST |IoPin.A_BEGIN, 'do({})'  , 15*m1pitch, 10*m1pitch,  8)
                         , (IoPin.EAST |IoPin.A_BEGIN, 'a({})'   , 10*m1pitch, 10*m1pitch, 16)
                         
                         , (IoPin.NORTH|IoPin.A_BEGIN, 'clk'     , 100*m2pitch,       0 ,  1)
                         , (IoPin.NORTH|IoPin.A_BEGIN, 'irq'     , 110*m2pitch,       0 ,  1)
                         , (IoPin.NORTH|IoPin.A_BEGIN, 'nmi'     , 120*m2pitch,       0 ,  1)
                         , (IoPin.NORTH|IoPin.A_BEGIN, 'rdy'     , 130*m2pitch,       0 ,  1)
                         , (IoPin.NORTH|IoPin.A_BEGIN, 'we'      , 140*m2pitch,       0 ,  1)
                         , (IoPin.NORTH|IoPin.A_BEGIN, 'reset'   , 150*m2pitch,       0 ,  1)
                         ]
        conf = ChipConf( cell, ioPins=ioPinsSpec, ioPads=ioPadsSpec ) 
       #conf.cfg.etesian.bloat               = 'Flexlib'
        conf.cfg.etesian.uniformDensity      = True
        conf.cfg.etesian.aspectRatio         = 1.0
       # etesian.spaceMargin is ignored if the coreSize is directly set.
        conf.cfg.etesian.spaceMargin         = 0.02
        conf.cfg.anabatic.searchHalo         = 2
        conf.cfg.anabatic.globalIterations   = 20
        conf.cfg.anabatic.topRoutingLayer    = 'm4'
        conf.cfg.katana.hTracksReservedLocal = 6
        conf.cfg.katana.vTracksReservedLocal = 3
        conf.cfg.katana.hTracksReservedMin   = 3
        conf.cfg.katana.vTracksReservedMin   = 1
        conf.cfg.katana.trackFill            = 0
        conf.cfg.katana.runRealignStage      = True
        conf.cfg.katana.dumpMeasures         = True
        conf.cfg.block.spareSide             = u(7*12)
        conf.cfg.chip.minPadSpacing          = u(1.46)
        conf.cfg.chip.supplyRailWidth        = u(20.0)
        conf.cfg.chip.supplyRailPitch        = u(40.0)
        if buildChip:
            conf.cfg.harness.path            = harnessProjectDir + '/user_project_wrapper.def'
        conf.editor              = editor
        conf.useSpares           = True
        conf.useClockTree        = True
        conf.useHFNS             = True
        conf.bColumns            = 2
        conf.bRows               = 2
        conf.chipName            = 'chip'
        conf.coreSize            = ( u( 27*12.0), u( 27*12.0) )
        conf.chipSize            = ( u(  2020.0), u(  2060.0) )
        if buildChip:
            conf.useHTree( 'io_in_from_pad(0)', Spares.HEAVY_LEAF_LOAD )
            conf.useHTree( 'io_in_from_pad(28)' )
        else:
            conf.useHTree( 'clk', Spares.HEAVY_LEAF_LOAD )
            conf.useHTree( 'reset' )
        #conf.useHTree( 'core.subckt_0_cpu.abc_11829_new_n340' )
        if buildChip:
            arlet6502ToChip = CoreToChip( conf )
            arlet6502ToChip.buildChip()
            if editor:
                editor.setCell( conf.chip )
            chipBuilder = Chip( conf )
            chipBuilder.doChipFloorplan()
            rvalue = chipBuilder.doPnR()
            chipBuilder.save()
        else:
            blockBuilder = Block( conf )
            rvalue = blockBuilder.doPnR()
            blockBuilder.save()
    except Exception as e:
        helpers.io.catch( e )
        rvalue = False
    sys.stdout.flush()
    sys.stderr.flush()
    return rvalue


if __name__ == '__main__':
    rvalue = scriptMain()
    shellRValue = 0 if rvalue else 1
    sys.exit( shellRValue )
