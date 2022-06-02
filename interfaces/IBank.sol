pragma solidity ^0.8.0;
interface IBank {
    function nextPositionId() external view returns(uint256);
    function positions(uint256 posId) external view returns(address,address,uint256,uint256,uint256);
    function getCollateralETHValue(uint256 posId) external view returns(uint256);
    function getPositionDebts(uint256 posId) external view returns(address[] memory, uint256[] memory);
}