// TypeScript interfaces matching backend Pydantic models

export type Mode = 'ionian' | 'dorian' | 'phrygian' | 'lydian' | 'mixolydian' | 'aeolian' | 'locrian';

export type VoiceRange = 'soprano' | 'alto' | 'tenor' | 'bass';

export type SpeciesType = 'first' | 'second' | 'third' | 'fourth' | 'fifth';

export interface GenerateCantusFirmusRequest {
  tonic: number;
  mode: Mode;
  length: number;
  voice_range: VoiceRange;
  seed?: number;
}

export interface Note {
  midi: number;
  duration: string;
}

export interface GenerateCantusFirmusResponse {
  notes: Note[];
  voice_range: VoiceRange;
  tonic?: number;
  mode?: Mode;
}

export interface GenerateCounterpointRequest {
  tonic: number;
  mode: Mode;
  cf_notes: number[];
  cf_voice_range: VoiceRange;
  seed?: number;
}

export interface GenerateMultiVoiceRequest {
  tonic: number;
  mode: Mode;
  cf_notes: number[];
  cf_voice_range: VoiceRange;
  num_voices: number;
  use_bass?: boolean;
  seed?: number;
}

export interface Voice {
  voice_index: number;
  voice_range: VoiceRange;
  notes: Note[];
}

export interface GenerateMultiVoiceResponse {
  voices: Voice[];
  num_voices: number;
}

export interface GenerateCounterpointResponse {
  cf_notes: number[];
  cp_notes: number[];
  cf_voice_range?: VoiceRange;
  cp_voice_range?: VoiceRange;
  tonic?: number;
  mode?: Mode;
}

export interface EvaluateCounterpointRequest {
  tonic: number;
  mode: Mode;
  cf_notes: number[];
  cp_notes: number[];
}

export interface RuleViolation {
  rule_code: string;
  description: string;
  voice_indices: number[];
  note_indices: number[];
  severity: 'info' | 'warning' | 'error';
}

export interface EvaluateCounterpointResponse {
  violations: RuleViolation[];
  is_valid: boolean;
  total_violations: number;
}
