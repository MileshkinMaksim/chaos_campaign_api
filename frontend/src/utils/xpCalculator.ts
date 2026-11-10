export const GUNNERY_UPGRADE_COSTS: Record<number, number> = {
  4: 300,  // 4 -> 3
  3: 700,  // 3 -> 2
  2: 1200, // 2 -> 1
  1: 2200, // 1 -> 0
};

export const PILOTING_UPGRADE_COSTS: Record<number, number> = {
  5: 100,  // 5 -> 4
  4: 200,  // 4 -> 3
  3: 700,  // 3 -> 2
  2: 1200, // 2 -> 1
};

export const EDGE_UPGRADE_COSTS: Record<number, number> = {
  1: 60,   // 1 -> 2
  2: 120,
  3: 200,
  4: 300,
  5: 420,
  6: 560,
  7: 720,
  8: 900,
  9: 1100,
};

export const SPA_COSTS_BY_COUNT: number[] = [60, 180, 360, 600, 900];

export function getGunneryUpgradeCost(currentSkill: number): number | null {
  return GUNNERY_UPGRADE_COSTS[currentSkill] ?? null;
}

export function getPilotingUpgradeCost(currentSkill: number): number | null {
  return PILOTING_UPGRADE_COSTS[currentSkill] ?? null;
}

export function getEdgeUpgradeCost(currentEdge: number): number | null {
  return EDGE_UPGRADE_COSTS[currentEdge] ?? null;
}

export function getNextSPACost(currentAbilitiesCount: number): number | null {
  if (currentAbilitiesCount >= 5) return null; // Лимит: 5 спец-способностей
  return SPA_COSTS_BY_COUNT[currentAbilitiesCount];
}