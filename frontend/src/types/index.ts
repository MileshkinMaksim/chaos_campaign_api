export const Faction = {
  DRACONIS_COMBINE: "Draconis Combine",
  FEDERATED_SUNS: "Federated Suns",
  RAVEN_ALLIANCE: "Raven Alliance",
  CLAN_SEA_FOX: "Clan Sea Fox",
  REPUBLIC_OF_THE_SPHERE: "Republic of the Sphere",
  MERCENARY: "Mercenary"
} as const;

export type Faction = (typeof Faction)[keyof typeof Faction];

export const UnitStatus = {
  OPERATIONAL: "Operational",
  DAMAGED: "Damaged",
  DESTROYED: "Destroyed",
  TRULY_DESTROYED: "Truly Destroyed"
} as const;
export type UnitStatus = (typeof UnitStatus)[keyof typeof UnitStatus];

export const WeightClass = {
  LIGHT: "Light",
  MEDIUM: "Medium",
  HEAVY: "Heavy",
  ASSAULT: "Assault"
} as const;
export type WeightClass = (typeof WeightClass)[keyof typeof WeightClass];

export interface NamedPilot {
  id: string;
  force_id?: string | null;
  name: string;
  gunnery: number;
  piloting: number;
  experience_points: number;
  total_xp_earned: number;
  edge_points: number;
  special_abilities: string[];
  is_temporary_hire: boolean;
}

export interface MechUnit {
  id: string;
  force_id?: string | null;
  chassis: string;
  model: string;
  tonnage: number;
  weight_class: WeightClass;
  bv2: number;
  status: UnitStatus;
  assigned_pilot_id?: string | null;
}

export interface StartingMechSelection {
  chassis: string;
  model: string;
  tonnage: number;
  weight_class: WeightClass;
  bv2: number;
}

export interface ForceCreate {
  name: string;
  sponsoring_faction: Faction;
  starting_pilot_names: [string, string];
  selected_mechs: StartingMechSelection[];
}

export interface ForceResponse {
  id: string;
  owner_id: string;
  name: string;
  sponsoring_faction: Faction;
  support_points: number;
  reputation_score: number;
  units: MechUnit[];
  pilots: NamedPilot[];
}

export interface AssignPilotRequest {
  unit_id: string;
  pilot_id?: string | null;
}

export interface StartingFactionOption {
  faction: Faction;
  display_name: string;
  description: string;
  available_rat_mechs: StartingMechSelection[];
}

export interface StartingOptionsResponse {
  available_factions: StartingFactionOption[];
  max_starting_mechs: number;
  max_starting_bv2: number;
  starting_sp: number;
  starting_reputation: number;
  starting_pilots_count: number;
  starting_xp_per_pilot: number;
}