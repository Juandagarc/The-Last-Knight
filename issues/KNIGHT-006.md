# KNIGHT-006: Combat System & Combos

## Labels
`ai-ready`, `priority-high`, `player`, `combat`

## Estimate
4 hours

## Dependencies
- KNIGHT-005 (Player FSM)

## Objective
Implement the combat system with attack states, combo chains, hitbox generation, and damage dealing.

## Requirements

### 1. src/states/attack_state.py - Attack State with Combos
```python
"""
Attack state with combo system.

Manages attack chains and hitbox generation.
"""

from typing import Optional

import pygame

from src.states.state import State
from src.core.settings import ATTACK_COMBO_WINDOW


class AttackState(State):
    """
    Player attack state with combo system.
    
    Supports 3-hit combo chains with timing windows.
    """
    
    name = "attack"
    
    ATTACKS = {
        1: {"duration": 0.3, "damage": 10, "animation": "attack1"},
        2: {"duration": 0.35, "damage": 15, "animation": "attack2"},
        3: {"duration": 0.5, "damage": 25, "animation": "attack3"},
    }
    
    def __init__(self, player) -> None:
        super().__init__(player)
        self.attack_number = 1
        self.attack_timer = 0.0
        self.can_combo = False
        self.combo_buffered = False
        self.current_hitbox: Optional[pygame.Rect] = None
        self.hit_targets: set = set()
    
    def enter(self) -> None:
        """Enter attack state."""
        self.attack_timer = 0.0
        self.can_combo = False
        self.combo_buffered = False
        self.hit_targets.clear()
        self._create_attack_hitbox()
        
        attack = self.ATTACKS[self.attack_number]
        self.player.animation.play(attack["animation"], force_restart=True)
        self.player.physics.velocity.x *= 0.3
    
    def update(self, dt: float) -> Optional[str]:
        """Update attack state."""
        attack = self.ATTACKS[self.attack_number]
        self.attack_timer += dt
        
        # Enable combo window at 70% of attack duration
        if self.attack_timer >= attack["duration"] * 0.7:
            self.can_combo = True
        
        # Check for combo input
        if self.can_combo and self.player.input_handler.is_action_just_pressed("attack"):
            self.combo_buffered = True
        
        # Attack finished
        if self.attack_timer >= attack["duration"]:
            if self.combo_buffered and self.attack_number < 3:
                self.attack_number += 1
                self.enter()
                return None
            else:
                self.attack_number = 1
                if self.player.physics.on_ground:
                    return "idle"
                return "fall"
        
        return None
    
    def exit(self) -> None:
        """Exit attack state."""
        self.current_hitbox = None
    
    def _create_attack_hitbox(self) -> pygame.Rect:
        """Create attack hitbox based on facing direction."""
        hitbox_width = 40
        hitbox_height = 48
        
        if self.player.facing_right:
            x = self.player.hitbox.right
        else:
            x = self.player.hitbox.left - hitbox_width
        
        y = self.player.hitbox.centery - hitbox_height // 2
        
        self.current_hitbox = pygame.Rect(x, y, hitbox_width, hitbox_height)
        return self.current_hitbox
    
    def get_attack_hitbox(self) -> Optional[pygame.Rect]:
        """Get current attack hitbox."""
        return self.current_hitbox
    
    def get_damage(self) -> int:
        """Get current attack damage."""
        return self.ATTACKS[self.attack_number]["damage"]


class CombatManager:
    """
    Manages combat interactions between entities.
    """
    
    def __init__(self) -> None:
        self.player = None
        self.enemies = []
    
    def set_player(self, player) -> None:
        """Set player reference."""
        self.player = player
    
    def add_enemy(self, enemy) -> None:
        """Add enemy to combat system."""
        self.enemies.append(enemy)
    
    def remove_enemy(self, enemy) -> None:
        """Remove enemy from combat system."""
        if enemy in self.enemies:
            self.enemies.remove(enemy)
    
    def update(self) -> None:
        """Check for combat interactions."""
        self._check_player_attacks()
        self._check_enemy_attacks()
    
    def _check_player_attacks(self) -> None:
        """Check if player attack hits enemies."""
        if not self.player:
            return
        
        state = self.player.current_state
        if not hasattr(state, "get_attack_hitbox"):
            return
        
        hitbox = state.get_attack_hitbox()
        if not hitbox:
            return
        
        for enemy in self.enemies:
            if enemy in state.hit_targets:
                continue
            
            if hitbox.colliderect(enemy.hitbox):
                damage = state.get_damage()
                enemy.take_damage(damage)
                state.hit_targets.add(enemy)
    
    def _check_enemy_attacks(self) -> None:
        """Check if enemy attacks hit player."""
        if not self.player or self.player.invulnerable:
            return
        
        for enemy in self.enemies:
            if hasattr(enemy, "get_attack_hitbox"):
                hitbox = enemy.get_attack_hitbox()
                if hitbox and hitbox.colliderect(self.player.hitbox):
                    damage = enemy.get_damage() if hasattr(enemy, "get_damage") else 10
                    self.player.take_damage(damage)
```

## Acceptance Criteria

- [ ] Attack state generates hitbox during animation
- [ ] Combo system allows chaining 3 attacks
- [ ] Combo window opens late in attack animation
- [ ] Different attacks deal different damage
- [ ] CombatManager tracks player vs enemy hits
- [ ] Enemies take damage when hit
- [ ] Player invulnerability prevents damage
- [ ] Hitbox appears in front of facing direction
- [ ] All tests pass

## Test Cases

| Test ID | Description | Expected Result |
|---------|-------------|-----------------|
| TC-006-1 | Attack creates hitbox | Hitbox rect exists |
| TC-006-2 | Combo window timing | can_combo at 70% |
| TC-006-3 | Combo progression | attack_number increments |
| TC-006-4 | Damage values | 10, 15, 25 for attacks 1-3 |
| TC-006-5 | Enemy takes hit | health decreases |
| TC-006-6 | Invulnerability | No damage taken |
| TC-006-7 | Hitbox facing right | Hitbox to player's right |
| TC-006-8 | Hitbox facing left | Hitbox to player's left |
