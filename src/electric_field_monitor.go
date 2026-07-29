// Package weather implements real-time electric field mill sensor monitoring
// and Launch Commit Criteria (LCC) rule evaluation for pad weather gating.
package weather

import (
	"fmt"
	"math"
	"sync"
	"time"
)

// FieldMillSensor represents an electric field sensor reading at the pad
type FieldMillSensor struct {
	SensorID     string
	LocationName string
	FieldKVPerM  float64   // Electric field strength (kV/m)
	Timestamp    time.Time
}

// LCCWeatherState represents the complete pad weather state
type LCCWeatherState struct {
	MaxSurfaceWindKts   float64
	UpperWindKts        float64
	ElectricFieldKVPerM float64
	LightningStrikes10M int
	CloudCeilingFt      float64
	TemperatureF        float64
	PrecipitationAtPad  bool
}

// ElectricFieldMonitor tracks electric field strength across sensors
type ElectricFieldMonitor struct {
	mu          sync.RWMutex
	sensors     map[string]*FieldMillSensor
	thresholdKV float64
}

func NewElectricFieldMonitor(thresholdKV float64) *ElectricFieldMonitor {
	return &ElectricFieldMonitor{
		sensors:     make(map[string]*FieldMillSensor),
		thresholdKV: thresholdKV,
	}
}

func (m *ElectricFieldMonitor) UpdateSensor(id string, location string, fieldKV float64) {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.sensors[id] = &FieldMillSensor{
		SensorID:     id,
		LocationName: location,
		FieldKVPerM:  fieldKV,
		Timestamp:    time.Now(),
	}
}

func (m *ElectricFieldMonitor) MaxElectricField() float64 {
	m.mu.RLock()
	defer m.mu.RUnlock()
	maxField := 0.0
	for _, s := range m.sensors {
		if math.Abs(s.FieldKVPerM) > maxField {
			maxField = math.Abs(s.FieldKVPerM)
		}
	}
	return maxField
}

func (m *ElectricFieldMonitor) IsTriggeredLightningRisk() bool {
	return m.MaxElectricField() >= m.thresholdKV
}

// EvaluateLCC returns (IsGo, RuleViolations)
func EvaluateLCC(state LCCWeatherState) (bool, []string) {
	var violations []string

	if state.MaxSurfaceWindKts > 30.0 {
		violations = append(violations, fmt.Sprintf("Surface wind (%.1f kts > 30 kts)", state.MaxSurfaceWindKts))
	}
	if state.UpperWindKts > 140.0 {
		violations = append(violations, fmt.Sprintf("Upper wind shear (%.1f kts > 140 kts)", state.UpperWindKts))
	}
	if state.ElectricFieldKVPerM >= 1.5 {
		violations = append(violations, fmt.Sprintf("Electric field strength (%.2f kV/m >= 1.5 kV/m)", state.ElectricFieldKVPerM))
	}
	if state.LightningStrikes10M > 0 {
		violations = append(violations, fmt.Sprintf("Lightning within 10 nmi (%d strikes)", state.LightningStrikes10M))
	}
	if state.TemperatureF < 40.0 {
		violations = append(violations, fmt.Sprintf("Pad temperature (%.1f°F < 40°F)", state.TemperatureF))
	}
	if state.PrecipitationAtPad {
		violations = append(violations, "Precipitation detected at launch pad")
	}

	return len(violations) == 0, violations
}
