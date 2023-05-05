
from designflow.technos import setupSky130_c4m

setupSky130_c4m( '/users/outil/coriolis/coriolis-2.x/src/alliance-check-toolkit', '/users/outil/coriolis/coriolis-2.x/src/alliance-check-toolkit/pdkmaster/C4M.Sky130' )

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
rulePnR   = PnR     .mkRule( 'pnr'  , [ 'arlet6502_cts_r.gds'
                                      , 'arlet6502_cts_r.spi'
                                      , 'arlet6502_cts_r.vst' ]
                                    , [ruleB2V]
                                    , scriptMain )
ruleCgt   = PnR     .mkRule( 'cgt' )
ruleGds   = Alias   .mkRule( 'gds', [rulePnR] )
# ruleClean = Clean   .mkRule()
