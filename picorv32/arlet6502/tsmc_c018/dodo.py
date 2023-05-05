
from designflow.technos import setupTSMC_c180_c4m

setupTSMC_c180_c4m( checkToolkit='/users/outil/coriolis/coriolis-2.x/src/alliance-check-toolkit/', ndaTop=None )

DOIT_CONFIG = { 'verbosity' : 2 }

from designflow.pnr      import PnR
from designflow.yosys    import Yosys
from designflow.blif2vst import Blif2Vst
from designflow.alias    import Alias
from designflow.clean    import Clean
PnR.textMode  = True

from doDesign  import scriptMain

ruleYosys = Yosys   .mkRule( 'yosys', 'Arlet6502.v' )
ruleB2V   = Blif2Vst.mkRule( 'b2v'  , [ 'arlet6502.vst'
                                      , 'Arlet6502.spi' ]
                                    , [ruleYosys]
                                    , flags=0 )
rulePnR   = PnR     .mkRule( 'pnr'  , [ 'chip_r.gds'
                                      , 'chip_r.vst'
                                      , 'chip_r.spi'
                                      , 'chip.vst'
                                      , 'chip.spi'
                                      , 'corona_cts_r.vst'
                                      , 'corona_cts_r.spi'
                                      , 'corona.vst'
                                      , 'corona.spi'
                                      , 'arlet6502.spi'
                                      , 'arlet6502_cts.spi'
                                      , 'arlet6502_cts.vst' ]
                                    , [ruleB2V]
                                    , scriptMain )
ruleCgt   = PnR  .mkRule( 'cgt' )
ruleGds   = Alias.mkRule( 'gds', [rulePnR] )
ruleClean = Clean.mkRule( [ 'corona.00.density.histogram.dat'
                          , 'corona.00.density.histogram.plt'
                          , 'corona.katana.dat' ] )
