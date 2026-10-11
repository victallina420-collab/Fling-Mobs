
import { world, system } from "@minecraft/server";

const WAND_ID = "flingmobs:fling_wand";

// INSANE FLING POWER 🔥🚀
const FLING_HORIZONTAL = 12;
const FLING_VERTICAL = 10;

world.afterEvents.entityHitEntity.subscribe((event) => {
    const player = event.damagingEntity;
    const mob = event.hitEntity;

    // Only players can use the wand.
    if (player.typeId !== "minecraft:player") return;

    // Never launch other players.
    if (mob.typeId === "minecraft:player") return;

    // Check the item held in the player's main hand.
    const equipment = player.getComponent("minecraft:equippable");
    const heldItem = equipment?.getEquipment("Mainhand");

    if (!heldItem || heldItem.typeId !== WAND_ID) return;

    // Calculate the direction away from the player.
    const p = player.location;
    const m = mob.location;

    let dx = m.x - p.x;
    let dz = m.z - p.z;

    const length = Math.sqrt(dx * dx + dz * dz) || 1;

    dx /= length;
    dz /= length;

    // Apply the launch after the hit event.
    system.run(() => {
        try {
            mob.applyImpulse({
                x: dx * FLING_HORIZONTAL,
                y: FLING_VERTICAL,
                z: dz * FLING_HORIZONTAL
            });

            player.sendMessage("§b§lYEET!!! §r§fMob launched! 🚀");
        } catch (error) {
            // Ignore entities that cannot receive an impulse.
        }
    });
});

console.warn("Fling Mobs INSANE Edition loaded!");
