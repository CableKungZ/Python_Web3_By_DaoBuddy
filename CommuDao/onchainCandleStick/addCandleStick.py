import json
from web3 import Web3
import warnings
from urllib3.exceptions import InsecureRequestWarning
from web3.middleware import ExtraDataToPOAMiddleware
from decimal import Decimal
from web3.exceptions import TransactionNotFound
import time
import logging
import traceback


private_key = "apiKeyHere"
CMswapCandleChartAddress = "0x7a90f3F76E88D4A2079E90197DD2661B8FEcA9B6"
CMswapCandleChartABI = json.loads('[{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256[]","name":"timestamps","type":"uint256[]"},{"internalType":"uint256[]","name":"values","type":"uint256[]"}],"name":"addAreaSeries","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256[]","name":"timestamps","type":"uint256[]"},{"internalType":"uint256[]","name":"prices","type":"uint256[]"},{"internalType":"uint256[]","name":"volumes","type":"uint256[]"}],"name":"addCandleStickSeries","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"tokenAs","type":"address[]"},{"internalType":"address[]","name":"tokenBs","type":"address[]"},{"internalType":"uint256[][]","name":"timestampsList","type":"uint256[][]"},{"internalType":"uint256[][]","name":"pricesList","type":"uint256[][]"},{"internalType":"uint256[][]","name":"volumeList","type":"uint256[][]"}],"name":"addCandleStickSeriesBatch","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_chainID","type":"uint256"},{"internalType":"uint256","name":"blockNumber","type":"uint256"}],"name":"updateBlockTime","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"page","type":"uint256"},{"internalType":"uint256","name":"pageSize","type":"uint256"}],"name":"getAreaData","outputs":[{"internalType":"uint256[]","name":"timestamps","type":"uint256[]"},{"internalType":"uint256[]","name":"values","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"getAreaDataCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"page","type":"uint256"},{"internalType":"uint256","name":"pageSize","type":"uint256"}],"name":"getCandleData","outputs":[{"internalType":"uint256[]","name":"timestamps","type":"uint256[]"},{"internalType":"uint256[]","name":"prices","type":"uint256[]"},{"internalType":"uint256[]","name":"volumes","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"getCandleDataCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"lastUpdateBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]')

chartABI = json.loads('[{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256[]","name":"timestamps","type":"uint256[]"},{"internalType":"uint256[]","name":"values","type":"uint256[]"}],"name":"addAreaSeries","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256[]","name":"timestamps","type":"uint256[]"},{"internalType":"uint256[]","name":"opens","type":"uint256[]"},{"internalType":"uint256[]","name":"highs","type":"uint256[]"},{"internalType":"uint256[]","name":"lows","type":"uint256[]"},{"internalType":"uint256[]","name":"closes","type":"uint256[]"}],"name":"addCandleStickSeries","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"page","type":"uint256"},{"internalType":"uint256","name":"pageSize","type":"uint256"}],"name":"getAreaData","outputs":[{"internalType":"uint256[]","name":"timestamps","type":"uint256[]"},{"internalType":"uint256[]","name":"values","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"page","type":"uint256"},{"internalType":"uint256","name":"pageSize","type":"uint256"}],"name":"getCandleData","outputs":[{"internalType":"uint256[]","name":"timestamps","type":"uint256[]"},{"internalType":"uint256[]","name":"opens","type":"uint256[]"},{"internalType":"uint256[]","name":"highs","type":"uint256[]"},{"internalType":"uint256[]","name":"lows","type":"uint256[]"},{"internalType":"uint256[]","name":"closes","type":"uint256[]"}],"stateMutability":"view","type":"function"}]')
pumpABI = json.loads('[{"inputs":[{"internalType":"address","name":"_weth","type":"address"},{"internalType":"address","name":"_v3factory","type":"address"},{"internalType":"address","name":"_v3posManager","type":"address"},{"internalType":"uint256","name":"_initialETH","type":"uint256"},{"internalType":"uint160","name":"_sqrtX96Initial0","type":"uint160"},{"internalType":"uint160","name":"_sqrtX96Initial1","type":"uint160"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"INITIALTOKEN","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"createFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"string","name":"_logo","type":"string"},{"internalType":"string","name":"_desp","type":"string"}],"name":"createToken","outputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"createdTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"creator","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"desp","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"feeCollector","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_pool","type":"address"},{"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"graduate","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"graduateMcap","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"index","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"initialETH","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"isGraduate","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"logo","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_createFee","type":"uint256"}],"name":"setCreateFee","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_newFeeCollector","type":"address"}],"name":"setFeeCollector","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_graduateMcap","type":"uint256"}],"name":"setGraduateMcap","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_initialETH","type":"uint256"},{"internalType":"uint160","name":"_sqrtX96Initial0","type":"uint160"},{"internalType":"uint160","name":"_sqrtX96Initial1","type":"uint160"}],"name":"setInitialETH","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"sqrtX96Initial0","outputs":[{"internalType":"uint160","name":"","type":"uint160"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"sqrtX96Initial1","outputs":[{"internalType":"uint160","name":"","type":"uint160"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"v3factory","outputs":[{"internalType":"contract IUniswapV3Factory","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"v3posManager","outputs":[{"internalType":"contract INonfungiblePositionManager","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"weth","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"}]')
factoryABI = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint24","name":"fee","type":"uint24"},{"indexed":true,"internalType":"int24","name":"tickSpacing","type":"int24"}],"name":"FeeAmountEnabled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"oldOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnerChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":true,"internalType":"uint24","name":"fee","type":"uint24"},{"indexed":false,"internalType":"int24","name":"tickSpacing","type":"int24"},{"indexed":false,"internalType":"address","name":"pool","type":"address"}],"name":"PoolCreated","type":"event"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"}],"name":"createPool","outputs":[{"internalType":"address","name":"pool","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"int24","name":"tickSpacing","type":"int24"}],"name":"enableFeeAmount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint24","name":"","type":"uint24"}],"name":"feeAmountTickSpacing","outputs":[{"internalType":"int24","name":"","type":"int24"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint24","name":"","type":"uint24"}],"name":"getPool","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"parameters","outputs":[{"internalType":"address","name":"factory","type":"address"},{"internalType":"address","name":"token0","type":"address"},{"internalType":"address","name":"token1","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"int24","name":"tickSpacing","type":"int24"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_owner","type":"address"}],"name":"setOwner","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
ERC20ABI = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]')

warnings.simplefilter('ignore', InsecureRequestWarning)
kub_web3 = Web3(Web3.HTTPProvider("https://rpc.bitkubchain.io", {"verify": False}))
kub_web3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
cm_web3 = Web3(Web3.HTTPProvider("https://cm-rpc.jibl2.com", {"verify": False}))

cmSwapRouterABI = json.loads('[{"inputs":[{"internalType":"address","name":"_factoryV2","type":"address"},{"internalType":"address","name":"factoryV3","type":"address"},{"internalType":"address","name":"_positionManager","type":"address"},{"internalType":"address","name":"_WETH9","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH9","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"approveMax","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"approveMaxMinusOne","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"approveZeroThenMax","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"approveZeroThenMaxMinusOne","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"bytes","name":"data","type":"bytes"}],"name":"callPositionManager","outputs":[{"internalType":"bytes","name":"result","type":"bytes"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"bytes[]","name":"paths","type":"bytes[]"},{"internalType":"uint128[]","name":"amounts","type":"uint128[]"},{"internalType":"uint24","name":"maximumTickDivergence","type":"uint24"},{"internalType":"uint32","name":"secondsAgo","type":"uint32"}],"name":"checkOracleSlippage","outputs":[],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"uint24","name":"maximumTickDivergence","type":"uint24"},{"internalType":"uint32","name":"secondsAgo","type":"uint32"}],"name":"checkOracleSlippage","outputs":[],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMinimum","type":"uint256"}],"internalType":"struct IV3SwapRouter.ExactInputParams","name":"params","type":"tuple"}],"name":"exactInput","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMinimum","type":"uint256"},{"internalType":"uint160","name":"sqrtPriceLimitX96","type":"uint160"}],"internalType":"struct IV3SwapRouter.ExactInputSingleParams","name":"params","type":"tuple"}],"name":"exactInputSingle","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMaximum","type":"uint256"}],"internalType":"struct IV3SwapRouter.ExactOutputParams","name":"params","type":"tuple"}],"name":"exactOutput","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMaximum","type":"uint256"},{"internalType":"uint160","name":"sqrtPriceLimitX96","type":"uint160"}],"internalType":"struct IV3SwapRouter.ExactOutputSingleParams","name":"params","type":"tuple"}],"name":"exactOutputSingle","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"factoryV2","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"getApprovalType","outputs":[{"internalType":"enum IApproveAndCall.ApprovalType","name":"","type":"uint8"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"token0","type":"address"},{"internalType":"address","name":"token1","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256","name":"amount0Min","type":"uint256"},{"internalType":"uint256","name":"amount1Min","type":"uint256"}],"internalType":"struct IApproveAndCall.IncreaseLiquidityParams","name":"params","type":"tuple"}],"name":"increaseLiquidity","outputs":[{"internalType":"bytes","name":"result","type":"bytes"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"token0","type":"address"},{"internalType":"address","name":"token1","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"int24","name":"tickLower","type":"int24"},{"internalType":"int24","name":"tickUpper","type":"int24"},{"internalType":"uint256","name":"amount0Min","type":"uint256"},{"internalType":"uint256","name":"amount1Min","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"internalType":"struct IApproveAndCall.MintParams","name":"params","type":"tuple"}],"name":"mint","outputs":[{"internalType":"bytes","name":"result","type":"bytes"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"previousBlockhash","type":"bytes32"},{"internalType":"bytes[]","name":"data","type":"bytes[]"}],"name":"multicall","outputs":[{"internalType":"bytes[]","name":"","type":"bytes[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bytes[]","name":"data","type":"bytes[]"}],"name":"multicall","outputs":[{"internalType":"bytes[]","name":"","type":"bytes[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"bytes[]","name":"data","type":"bytes[]"}],"name":"multicall","outputs":[{"internalType":"bytes[]","name":"results","type":"bytes[]"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"positionManager","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"pull","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"refundETH","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermit","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitAllowed","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitAllowedIfNecessary","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitIfNecessary","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"name":"sweepToken","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountMinimum","type":"uint256"}],"name":"sweepToken","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"uint256","name":"feeBips","type":"uint256"},{"internalType":"address","name":"feeRecipient","type":"address"}],"name":"sweepTokenWithFee","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"feeBips","type":"uint256"},{"internalType":"address","name":"feeRecipient","type":"address"}],"name":"sweepTokenWithFee","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"int256","name":"amount0Delta","type":"int256"},{"internalType":"int256","name":"amount1Delta","type":"int256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"uniswapV3SwapCallback","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"name":"unwrapWETH9","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountMinimum","type":"uint256"}],"name":"unwrapWETH9","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"feeBips","type":"uint256"},{"internalType":"address","name":"feeRecipient","type":"address"}],"name":"unwrapWETH9WithFee","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"uint256","name":"feeBips","type":"uint256"},{"internalType":"address","name":"feeRecipient","type":"address"}],"name":"unwrapWETH9WithFee","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"value","type":"uint256"}],"name":"wrapETH","outputs":[],"stateMutability":"payable","type":"function"},{"stateMutability":"payable","type":"receive"}]')
cmSwapRouter = "0x3F7582E36843FF79F173c7DC19f517832496f2D8"

kub_PumpLiteAddress = "0x10d7c3bDc6652bc3Dd66A33b9DD8701944248c62"
kub_PumpBuildBlock = 25229488

kub_PumpProAddress = "0x7bdceEAf4F62ec61e2c53564C2DbD83DB2015a56"
kub_PumpProBuildBlock = 25232899

V3_KubADDr = "0x090C6E5fF29251B1eF9EC31605Bdd13351eA316C"
monad_PumpProAddress = "0x6dfc8eecca228c45cc55214edc759d39e5b39c93"

CMM = "0x9B005000A10Ac871947D99001345b01C1cEf2790"
KKUB = "0x67eBD850304c70d983B2d1b93ea79c7CD6c3F6b5"

logging.basicConfig(
    filename='log.txt',      
    level=logging.INFO,                   
    format='%(asctime)s - %(levelname)s - %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S'
)

def get_block_info(web3, tx_hash):
    try:
        receipt = web3.eth.get_transaction_receipt(tx_hash)
        block_number = receipt.blockNumber
        block = web3.eth.get_block(block_number)
        block_timestamp = block.timestamp
        return block_number, block_timestamp
    except Exception as e:
        print(f"⚠️ Error fetching block info for tx {tx_hash}: {e}")
        return 0, 0
    
def getPumpLite(web3: Web3, pump_address: str, factory_address: str, lastSync: int):
    pump_contract = web3.eth.contract(address=pump_address, abi=pumpABI)
    factory_contract = web3.eth.contract(address=factory_address, abi=factoryABI)

    result = []

    total_indexes = pump_contract.functions.totalIndex().call()

    for i in range(total_indexes):
        try:
            token_address = pump_contract.functions.index(i + 1).call()
            pool_address = factory_contract.functions.getPool(token_address, CMM, 10000).call()

            token_sell_txs, token_sell_vals,token_over_sell  = get_logs(web3, token_address, ERC20ABI, "Transfer",
                                                       argument_filters={"to": pool_address},
                                                       from_block=lastSync)
            token_buy_txs, token_buy_vals,token_over_buy  = get_logs(web3, token_address, ERC20ABI, "Transfer",
                                                     argument_filters={"from": pool_address},
                                                     from_block=lastSync)

            cmm_sell_txs, cmm_sell_vals,cmm_over_sell  = get_logs(web3, CMM, ERC20ABI, "Transfer",
                                                   argument_filters={"to": pool_address},
                                                   from_block=lastSync)
            cmm_buy_txs, cmm_buy_vals,cmm_over_buy  = get_logs(web3, CMM, ERC20ABI, "Transfer",
                                                 argument_filters={"from": pool_address},
                                                 from_block=lastSync)

            print(f"Token {i+1} - Total Sell logs: {len(token_sell_txs)}, Buy logs: {len(token_buy_txs)}")

            token_sell_map = dict(zip(token_sell_txs, token_sell_vals))
            token_buy_map = dict(zip(token_buy_txs, token_buy_vals))
            cmm_sell_map = dict(zip(cmm_sell_txs, cmm_sell_vals))
            cmm_buy_map = dict(zip(cmm_buy_txs, cmm_buy_vals))

            events = []

            # Sell Token แลก CMM
            common_sell_txs = set(token_sell_map.keys()) & set(cmm_buy_map.keys())
            for tx_hash, val in token_over_sell + token_over_buy + cmm_over_sell + cmm_over_buy:
                block_num, block_time = get_block_info(web3, tx_hash)
                price = 6000 / 1_000_000_000
                print(f"📢 Intitials Pool (Lite) TX {tx_hash} | Price: {price} | Block: {block_num} Time: {block_time}")
                events.append({"block": block_num, "timestamp": block_time, "price": price, "volume": 0})

            for tx in common_sell_txs:
                token_amount = token_sell_map[tx] / 1e18
                cmm_amount = cmm_buy_map[tx] / 1e18
                price = cmm_buy_map[tx] / token_sell_map[tx]

                block_num, block_time = get_block_info(web3, tx)
                print(f"Sell {token_amount:.6f} Token for {cmm_amount:.6f} CMM | @ {price:.18f} | Block: {block_num} Time: {block_time}")

                events.append({"block": block_num, "timestamp": block_time, "price": price, "volume": token_amount})

            # Buy Token โดยใช้ CMM
            common_buy_txs = set(token_buy_map.keys()) & set(cmm_sell_map.keys())
            for tx in common_buy_txs:
                token_amount = token_buy_map[tx] / 1e18
                cmm_amount = cmm_sell_map[tx] / 1e18
                price = cmm_sell_map[tx] / token_buy_map[tx]

                block_num, block_time = get_block_info(web3, tx)
                print(f"Buy {token_amount:.6f} Token for {cmm_amount:.6f} CMM | @ {price:.18f} | Block: {block_num} Time: {block_time}")

                events.append({"block": block_num, "timestamp": block_time, "price": price, "volume": token_amount})

            if events:
                result.append({ 
                    "token": token_address,
                    "events": events
                })

        except Exception as e:
            print(f"⚠️ Error processing token index {i + 1}: {e}")

    print(f"✅ Total tokens processed: {len(result)}")
    return result

def getPumpPro(web3: Web3, pump_address: str, factory_address: str, lastSync: int):
    pump_contract = web3.eth.contract(address=pump_address, abi=pumpABI)
    factory_contract = web3.eth.contract(address=factory_address, abi=factoryABI)

    result = []
    total_indexes = pump_contract.functions.totalIndex().call()

    for i in range(total_indexes):
        try:
            token_address = pump_contract.functions.index(i + 1).call()
            pool_address = factory_contract.functions.getPool(token_address, KKUB, 10000).call()

            token_sell_txs, token_sell_vals,token_over_sell = get_logs(web3, token_address, ERC20ABI, "Transfer",
                                                       argument_filters={"to": pool_address},
                                                       from_block=lastSync)
            token_buy_txs, token_buy_vals,token_over_buy = get_logs(web3, token_address, ERC20ABI, "Transfer",
                                                     argument_filters={"from": pool_address},
                                                     from_block=lastSync)

            kkub_sell_txs, kkub_sell_vals,kkub_over_sell = get_logs(web3, KKUB, ERC20ABI, "Transfer",
                                                   argument_filters={"to": pool_address},
                                                   from_block=lastSync)
            kkub_buy_txs, kkub_buy_vals,kkub_over_buy  = get_logs(web3, KKUB, ERC20ABI, "Transfer",
                                                 argument_filters={"from": pool_address},
                                                 from_block=lastSync)

            print(f"Token {i+1} - Total Sell logs: {len(token_sell_txs)}, Buy logs: {len(token_buy_txs)}")

            token_sell_map = dict(zip(token_sell_txs, token_sell_vals))
            token_buy_map = dict(zip(token_buy_txs, token_buy_vals))
            kkub_sell_map = dict(zip(kkub_sell_txs, kkub_sell_vals))
            kkub_buy_map = dict(zip(kkub_buy_txs, kkub_buy_vals))

            events = []

            # Sell Token แลก KKUB
            common_sell_txs = set(token_sell_map.keys()) & set(kkub_buy_map.keys())
            for tx_hash, val in token_over_sell + token_over_buy + kkub_over_sell + kkub_over_buy:
                block_num, block_time = get_block_info(web3, tx_hash)
                price = 1 / 1_000_000_000
                print(f"📢 Intitals Pool at TX {tx_hash} | Price: {price} | Block: {block_num} Time: {block_time}")
                events.append({"block": block_num, "timestamp": block_time, "price": price, "volume": 0})
            for tx in common_sell_txs:
                token_amount = token_sell_map[tx] / 1e18
                kkub_amount = kkub_buy_map[tx] / 1e18
                price = kkub_buy_map[tx] / token_sell_map[tx]

                block_num, block_time = get_block_info(web3, tx)
                print(f"Sell {token_amount:.6f} Token for {kkub_amount:.6f} KKUB | @ {price:.18f} | Block: {block_num} Time: {block_time}")

                events.append({"block": block_num, "timestamp": block_time, "price": price, "volume": token_amount})

            # Buy Token โดยใช้ KKUB
            common_buy_txs = set(token_buy_map.keys()) & set(kkub_sell_map.keys())
            for tx in common_buy_txs:
                token_amount = token_buy_map[tx] / 1e18
                kkub_amount = kkub_sell_map[tx] / 1e18
                price = kkub_sell_map[tx] / token_buy_map[tx]

                block_num, block_time = get_block_info(web3, tx)
                print(f"Buy {token_amount:.6f} Token for {kkub_amount:.6f} KKUB | @ {price:.18f} | Block: {block_num} Time: {block_time}")

                events.append({"block": block_num, "timestamp": block_time, "price": price, "volume": token_amount})
            if events:
                result.append({
                    "token": token_address,
                    "events": events
                })

        except Exception as e:
            print(f"⚠️ Error processing token index {i + 1}: {e}")

    print(f"✅ Total tokens processed: {len(result)}")
    return result

def get_logs(web3, contract_address, abi, event_name, from_block='latest', to_block='latest', argument_filters=None):
    contract = web3.eth.contract(address=contract_address, abi=abi)
    event = getattr(contract.events, event_name)

    try:
        logs = event().get_logs(
            from_block=from_block,
            to_block=to_block,
            argument_filters=argument_filters or {}
        )
    except Exception as e:
        print(f"⚠️ Error fetching logs for {contract_address}: {e}")
        return [], [], []

    filtered = [(log.transactionHash.hex(), log.args.value) for log in logs if log.args.value < 999999999999999999999999000]
    over_filtered = [(log.transactionHash.hex(), log.args.value) for log in logs if log.args.value > 999999999999999999999999000]
    
    if not filtered and not over_filtered:
        return [], [], []

    if filtered:
        txhashes, values = zip(*filtered)
        return list(txhashes), list(values), over_filtered
    return [], [], over_filtered

def featData(web3, raw_data,pair, chainId):
    contract = web3.eth.contract(address=CMswapCandleChartAddress, abi=CMswapCandleChartABI)
    address = web3.eth.account.from_key(private_key).address

    tokenAs = []
    tokenBs = []
    timestampsList = []
    pricesList = []
    volumeList = []

    for token_info in raw_data:
        token = token_info["token"]
        events = token_info["events"]

        timestamps = []
        prices = []
        volumes = []

        for event in events:
            timestamps.append(event.get("timestamp", 0))
            prices.append(int(Decimal(str(event["price"])) * Decimal(1e18)))
            volumes.append(int(Decimal(str(event["volume"])) * Decimal(1e18)))

        tokenAs.append(token)
        tokenBs.append(pair) 
        timestampsList.append(timestamps)
        pricesList.append(prices)
        volumeList.append(volumes)

    nonce = web3.eth.get_transaction_count(address)

    print(tokenAs)
    print(tokenBs)
    print(timestampsList)
    print(pricesList)
    print(volumeList)

    tx = contract.functions.addCandleStickSeriesBatch(
        tokenAs,
        tokenBs,
        timestampsList,
        pricesList,
        volumeList
    ).build_transaction({
        'from': address,
        'nonce': nonce,
        'gas': 8_000_000,
        'gasPrice': web3.to_wei('0.00000001', 'gwei'),
        'chainId': 88991001
    })

    signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"✅ addCandleStickSeriesBatch Tx sent: {tx_hash.hex()}")

    while True:
        try:
            receipt = cm_web3.eth.get_transaction_receipt(tx_hash)
            if receipt is not None:
                if receipt.status == 1:
                    print(f"✅ Confirmed: {tx_hash.hex()} in block {receipt.blockNumber}")
                else:
                    print(f"❌ Transaction failed: {tx_hash.hex()}")
                break
        except TransactionNotFound:
            time.sleep(0.1)

    max_block = max([max([e["block"] for e in token_info["events"]] or [0]) for token_info in raw_data] or [0])
 
def updateBlock(chainId,_block):
    contract = cm_web3.eth.contract(address=CMswapCandleChartAddress, abi=CMswapCandleChartABI)
    address = kub_web3.eth.account.from_key(private_key).address

    tx2 = contract.functions.updateBlockTime(chainId, _block).build_transaction({
            'from': address,
            'nonce': cm_web3.eth.get_transaction_count(address),
            'gas': 500_000,
            'gasPrice': cm_web3.to_wei('0.00000001', 'gwei'),
            'chainId': 88991001
        })

    signed_tx2 = cm_web3.eth.account.sign_transaction(tx2, private_key=private_key)
    tx_hash2 = cm_web3.eth.send_raw_transaction(signed_tx2.raw_transaction)
    print(f"✅ updateBlockTime Tx sent: {tx_hash2.hex()}")
    while True:
        try:
            receipt = cm_web3.eth.get_transaction_receipt(tx_hash2)
            if receipt is not None:
                if receipt.status == 1:
                    print(f"✅ Confirmed: {tx_hash2.hex()} in block {receipt.blockNumber}")
                else:
                    print(f"❌ Transaction failed: {tx_hash2.hex()}")
                break
        except TransactionNotFound:
            time.sleep(0.1)

def save_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

def worker():

    lastSyncBlock_KUB = getHistory(96)
    print(f"Last KUBchain Sync {lastSyncBlock_KUB}")

    print(f"Fetching Pump Lite Data...")
    pump_lite_data = getPumpLite(kub_web3, kub_PumpLiteAddress, V3_KubADDr,lastSyncBlock_KUB)
    print(f"Fetching Pump Pro Data...")
    pump_pro_data = getPumpPro(kub_web3, kub_PumpProAddress, V3_KubADDr,lastSyncBlock_KUB)


    if pump_lite_data and len(pump_lite_data) > 0:
        featData(cm_web3, pump_lite_data, CMM, 96)
        time.sleep(5)
        
    if pump_pro_data and len(pump_pro_data) > 0:
        featData(cm_web3, pump_pro_data, KKUB, 96)
        time.sleep(5)
    
    current_block = kub_web3.eth.block_number
    updateBlock(96, current_block)
    print("Sleep for 5 mins.")
    time.sleep(300) ## Update every 5 minutes




def getHistory(chainId):
    contract = cm_web3.eth.contract(address=CMswapCandleChartAddress, abi=CMswapCandleChartABI)
    lastSyncKUB = contract.functions.lastUpdateBlock(chainId).call()
    return lastSyncKUB


if __name__ == "__main__":
    try:
        while True:
            worker()
            time.sleep(60) 
    except Exception as e:
        logging.error("Bot down: %s", str(e))
        logging.error(traceback.format_exc()) 
        print(f"Bot down: with reason {e}")
