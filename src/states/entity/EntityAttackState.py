import pygame
from src.states.BaseState import BaseState

class EntityAttackState(BaseState):
    def __init__(self, entity):
        self.entity = entity
        self.attack_timer = 0

    def Enter(self, params):
        direction = self.entity.direction_x
        self.entity.ChangeAnimation(f"attack_{direction}")
        self.attack_timer = 0  # Reset attack timer

    def Exit(self):
        pass

    def update(self, dt, events):
        self.attack_timer += dt

        # Perform attack logic during animation
        if self.attack_timer > 0.5:  # Example: Attack every 0.5 seconds
            if self.entity.target and self.entity.Collides(self.entity.target) and not self.entity.target.invulnerable:
                self.entity.Attack(self.entity.target)
                self.entity.target.SetInvulnerable(0.5)

        # Return to walk after attack animation finishes
        if self.entity.curr_animation.times_played > 0:
            self.entity.ChangeState("walk")

    def render(self, screen):
        animation = self.entity.curr_animation.image
        screen.blit(animation, (self.entity.x, self.entity.y))
