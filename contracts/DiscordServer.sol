// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DiscordServer {
    struct Channel {
        string name;
        address[] members;
    }

    mapping(string => Channel) public channels;
    mapping(address => string) public usernames;

    function createChannel(string memory _name) public {
        Channel storage c = channels[_name];
        c.name = _name;
        c.members.push(msg.sender);
    }

    function joinChannel(string memory _name) public {
        channels[_name].members.push(msg.sender);
    }

    function setUsername(string memory _username) public {
        usernames[msg.sender] = _username;
    }
}
