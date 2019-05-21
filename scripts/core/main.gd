"""
Main entry point for the game. Based on the current settings,
we may have this do different things.
"""
extends Node2D

# -- Imports
const CampaignLoader = preload("campaign.gd");
const Player         = preload("player.gd");

# -- Development Flags
var DEV_MODE: bool = true;

# -- Memebers
onready var _player = Player.new();
onready var _campaign_loader = CampaignLoader.new();

func _ready():
    """
    The function that starts it all!
    """
    add_child(_player);
    add_child(_campaign_loader);

    if DEV_MODE:
        _campaign_loader._basic_start(_player);