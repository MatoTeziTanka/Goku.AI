// ============================================================================
// SHENRON SYNDICATE v3.3 - Complete Frontend JavaScript  
// ============================================================================
// Features:
// - v3.2.2: Fixed warrior status animations (turn green individually)
// - v3.3: Live clock with user location
// - v3.3: Version info and last update date
// - v3.3: Enhanced DBZ easter eggs
// ============================================================================

const API_BASE = "/api.php";
let lastPythonHeartbeat = null;
const jobEventKeys = [];
const jobEventMax = 60;

const WARRIORS = {
    goku: { emoji: "🥋", name: "GOKU", role: "Adaptive Warrior & Growth Catalyst" },
    vegeta: { emoji: "👑", name: "VEGETA", role: "Technical Authority" },
    piccolo: { emoji: "🧠", name: "PICCOLO", role: "Strategic Sage" },
    gohan: { emoji: "⚠️", name: "GOHAN", role: "Risk Sentinel" },
    krillin: { emoji: "🔧", name: "KRILLIN", role: "Practical Engineer" },
    frieza: { emoji: "😈", name: "FRIEZA", role: "Chaos Tyrant" }
};

// ============================================================================
// POWER MODE CONFIGURATION - ULTRA INSTINCT
// ============================================================================

const POWER_MODES = {
    lightning: {
        name: 'LIGHTNING MODE',
        icon: '⚡',
        power: '1,000',
        warriors: 1,
        accuracy: '85-90%',
        time: '5-10s',
        color: '#f1c40f',
        description: 'Fast single-warrior response'
    },
    council: {
        name: 'COUNCIL MODE',
        icon: '🔥',
        power: '9,000',
        warriors: 6,
        accuracy: '95-99%',
        time: '20-40s',
        color: '#e74c3c',
        description: 'Balanced consensus & synthesis'
    },
    ultra: {
        name: 'ULTRA INSTINCT MODE',
        icon: '🐉',
        power: 'OVER 9000!',
        warriors: 6,
        accuracy: '99.99999999%',
        time: '60-180s',
        color: '#9b59b6',
        description: 'Maximum accuracy multi-pass'
    }
};

// Agent Mode & Power Mode state
let agentModeEnabled = false;
let agentModeVerified = false;
let agentMode2FAExpires = null;
let selectedPowerMode = 'auto'; // 'auto', 'lightning', 'council', 'ultra'
let detectedPowerMode = 'council'; // auto-detected mode
let agentConsoleVisible = false;
let consoleMinimized = false;
let metricsInterval = null;
const WARRIOR_KEYS = Object.keys(WARRIORS);
let shenronOverlayTimer = null;
let shenronUnlocked = false;
let powerBurstCooldown = false;
let visualEffectsEnabled = localStorage.getItem('dragonRadarVisuals') !== 'minimal';
const warriorHealthState = {};
let activeWish = null;
let lightningWatchdogTimer = null;
let lightningWarningShown = false;

// Track animation timeouts for cleanup
let animationTimeouts = [];

class DragonRadarSoundboard {
    constructor() {
        this.enabled = localStorage.getItem('dragonRadarAudio') !== 'muted';
        this.ctx = null;
        this.masterGain = null;
        this.toggleBtn = null;
        this.sequences = {
            start: [
                { freq: 220, duration: 0.12 },
                { gap: 0.02 },
                { freq: 330, duration: 0.12 },
                { gap: 0.02 },
                { freq: 440, duration: 0.18 },
                { gap: 0.01 },
                { freq: 660, duration: 0.2, volume: 0.8 }
            ],
            'warrior-complete': [
                { freq: 880, duration: 0.13, volume: 0.85 },
                { gap: 0.03 },
                { freq: 988, duration: 0.1, volume: 0.6 }
            ],
            'all-complete': [
                { freq: 523, duration: 0.12 },
                { gap: 0.03 },
                { freq: 659, duration: 0.12 },
                { gap: 0.03 },
                { freq: 784, duration: 0.12 },
                { gap: 0.04 },
                { freq: 1046, duration: 0.28, volume: 0.9 }
            ],
            error: [
                { freq: 180, duration: 0.18, type: 'sawtooth', volume: 0.6 },
                { gap: 0.04 },
                { freq: 150, duration: 0.22, type: 'triangle', volume: 0.5 }
            ],
            'critical-error': [
                { freq: 120, duration: 0.22, type: 'square', volume: 0.7 },
                { gap: 0.04 },
                { freq: 90, duration: 0.25, type: 'square', volume: 0.7 },
                { gap: 0.05 },
                { freq: 60, duration: 0.3, type: 'sine', volume: 0.5 }
            ],
            'shenron-summon': [
                { freq: 392, duration: 0.18, volume: 0.7 },
                { gap: 0.04 },
                { freq: 523, duration: 0.2, volume: 0.8 },
                { gap: 0.05 },
                { freq: 659, duration: 0.28, volume: 0.9 },
                { gap: 0.02 },
                { freq: 784, duration: 0.3, volume: 0.95 }
            ],
            toggle: [
                { freq: 660, duration: 0.08, volume: 0.5 },
                { gap: 0.04 },
                { freq: 880, duration: 0.08, volume: 0.5 }
            ]
        };
    }

    init() {
        if (this.ctx) return;
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return;
        this.ctx = new AudioCtx();
        this.masterGain = this.ctx.createGain();
        this.masterGain.gain.value = 0.35;
        this.masterGain.connect(this.ctx.destination);
    }

    unlock() {
        if (!this.enabled) return;
        this.init();
        if (this.ctx && this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
    }

    ensureContext() {
        if (!this.enabled) return Promise.resolve();
        this.init();
        if (!this.ctx) return Promise.resolve();
        if (this.ctx.state === 'suspended') {
            return this.ctx.resume();
        }
        return Promise.resolve();
    }

    play(type) {
        if (!this.enabled) return;
        const sequence = this.sequences[type];
        if (!sequence) return;
        this.ensureContext().then(() => {
            if (!this.ctx || !this.masterGain) return;
            let time = this.ctx.currentTime;
            sequence.forEach(note => {
                if (note.gap) {
                    time += note.gap;
                    return;
                }
                this.playTone({
                    frequency: note.freq,
                    duration: note.duration,
                    start: time,
                    type: note.type || 'sine',
                    volume: note.volume || 1
                });
                time += note.duration + (note.gap || 0);
            });
        }).catch(() => {});
    }

    playTone({ frequency, duration, start, type, volume }) {
        if (!this.ctx || !this.masterGain) return;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(frequency, start);

        const v = Math.max(0, Math.min(1, volume));
        gain.gain.setValueAtTime(this.masterGain.gain.value * v, start);
        gain.gain.exponentialRampToValueAtTime(0.0001, start + duration);

        osc.connect(gain);
        gain.connect(this.masterGain);

        osc.start(start);
        osc.stop(start + duration + 0.02);
    }

    registerToggle(btn) {
        if (!btn) return;
        this.toggleBtn = btn;
        btn.addEventListener('click', () => {
            this.setEnabled(!this.enabled);
            if (this.enabled) {
                this.unlock();
                this.play('toggle');
            }
        });
        this.refreshToggleUI();
    }

    setEnabled(flag) {
        this.enabled = flag;
        localStorage.setItem('dragonRadarAudio', flag ? 'on' : 'muted');
        this.refreshToggleUI();
    }

    refreshToggleUI() {
        if (!this.toggleBtn) return;
        if (this.enabled) {
            this.toggleBtn.classList.remove('muted');
            this.toggleBtn.textContent = '🔊';
        } else {
            this.toggleBtn.classList.add('muted');
            this.toggleBtn.textContent = '🔈';
        }
    }
}

const Soundboard = new DragonRadarSoundboard();

function playSound(type) {
    Soundboard.play(type);
}

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

function setScreenAura(mode) {
    const body = document.body;
    body.classList.remove('mode-lightning', 'mode-council', 'mode-ultra');
    if (!mode) return;
    const map = {
        lightning: 'mode-lightning',
        council: 'mode-council',
        ultra: 'mode-ultra'
    };
    const cls = map[mode];
    if (cls) body.classList.add(cls);
}

function setRadarActive(active) {
    const panel = document.getElementById('metrics-panel');
    if (!panel) return;
    if (!active) {
        panel.classList.remove('radar-active', 'power-burst');
    } else {
        panel.classList.add('radar-active');
    }
}

function updateRadarSpeed(progressValue) {
    const radar = document.querySelector('.metric-radar');
    if (!radar) return;
    const clamped = Math.max(0, Math.min(100, progressValue || 0));
    const speed = Math.max(1.6, 4 - (clamped / 35));
    radar.style.setProperty('--radar-speed', `${speed}s`);
}

function triggerPowerBurst() {
    if (powerBurstCooldown) return;
    const panel = document.getElementById('metrics-panel');
    if (!panel) return;
    powerBurstCooldown = true;
    panel.classList.add('power-burst');
    setTimeout(() => {
        panel.classList.remove('power-burst');
        powerBurstCooldown = false;
    }, 700);
}

function triggerRadarPing() {
    const radar = document.querySelector('.metric-radar');
    if (!radar) return;
    const blip = document.createElement('div');
    blip.className = 'radar-ping-blip';
    const angle = Math.random() * 360;
    const distance = 18 + Math.random() * 30;
    blip.style.setProperty('--blip-angle', `${angle}deg`);
    blip.style.setProperty('--blip-distance', `${distance}px`);
    radar.appendChild(blip);
    setTimeout(() => blip.remove(), 1200);
}

function refreshDragonBallStrip() {
    const balls = document.querySelectorAll('.dragon-ball');
    if (!balls.length) return;
    const completedCount = WARRIOR_KEYS.filter(key => {
        const statusEl = document.getElementById(`status-${key}`);
        return statusEl?.classList.contains('done');
    }).length;

    balls.forEach((ball, index) => {
        if (index < completedCount) {
            ball.classList.add('active');
        } else {
            ball.classList.remove('active', 'shenron-ready');
        }
    });

    const finalBall = balls[balls.length - 1];
    if (completedCount >= WARRIOR_KEYS.length) {
        if (!shenronUnlocked) {
            shenronUnlocked = true;
            finalBall.classList.add('active', 'shenron-ready');
            showShenronOverlay();
        }
    } else {
        shenronUnlocked = false;
        finalBall?.classList.remove('shenron-ready');
        hideShenronOverlay();
    }
}

function initializeWarriorHealthState() {
    WARRIOR_KEYS.forEach(key => {
        warriorHealthState[key] = {
            state: 'idle',
            responseTime: null,
            text: 'Ready',
            updatedAt: Date.now()
        };
    });
    renderWarriorHealthSummary();
}

function renderWarriorHealthSummary() {
    const container = document.getElementById('metric-warrior-health');
    if (!container) return;
    const fragments = WARRIOR_KEYS.map(key => {
        const warrior = WARRIORS[key];
        const stateEntry = warriorHealthState[key] || {};
        const state = stateEntry.state || 'idle';
        const responseTime = stateEntry.responseTime;
        const statusTextMap = {
            idle: 'Ready',
            thinking: 'Consulting',
            done: 'Complete',
            error: 'Issue'
        };
        const statusText = statusTextMap[state] || state;
        const meta = typeof responseTime === 'number'
            ? `${responseTime.toFixed(1)}s`
            : (state === 'thinking' ? '...' : '');
        return `
            <div class="warrior-badge ${state}" data-warrior="${key}">
                <span class="badge-emoji">${warrior.emoji}</span>
                <span class="badge-name">${warrior.name}</span>
                <span class="badge-status">${statusText}</span>
                ${meta ? `<span class="badge-meta">${meta}</span>` : ''}
            </div>
        `;
    });
    container.innerHTML = fragments.join('');
}

function updateProgressWarning(message, tone = 'warning') {
    const warningEl = document.getElementById('progress-warning');
    const textEl = document.getElementById('progress-warning-text');
    if (!warningEl || !textEl) return;

    warningEl.classList.remove('tone-warning', 'tone-info', 'tone-error');

    if (!message) {
        warningEl.classList.add('hidden');
        warningEl.removeAttribute('data-tone');
        return;
    }

    warningEl.classList.remove('hidden');
    warningEl.setAttribute('data-tone', tone);
    warningEl.classList.add(`tone-${tone}`);
    textEl.textContent = message;
}

function hideProgressWarning() {
    updateProgressWarning(null);
}

function showPendingActions(actions) {
    if (!Array.isArray(actions) || actions.length === 0) {
        hideProgressWarning();
        return;
    }

    const summary = actions.map((action, index) => {
        const label = action?.source ? `${action.source}` : `Action ${index + 1}`;
        const detail = action?.summary || action?.status || 'Follow-up required';
        return `${index + 1}. ${label}: ${detail}`;
    }).join(' • ');

    updateProgressWarning(`Follow-up required – ${summary}`, 'warning');
}

function startLightningWatchdog() {
    clearLightningWatchdog();
    lightningWarningShown = false;
    lightningWatchdogTimer = setTimeout(() => {
        lightningWarningShown = true;
        updateProgressWarning('Lightning Mode is taking longer than expected. You can wait or cancel and rerun in Council Mode.', 'warning');
        if (agentModeEnabled && agentConsoleVisible) {
            logToConsole('⚠️ Lightning Mode exceeded 2 minutes. Consider upgrading to Council Mode.', 'warning');
        }
    }, 120000);
}

function clearLightningWatchdog() {
    if (lightningWatchdogTimer) {
        clearTimeout(lightningWatchdogTimer);
        lightningWatchdogTimer = null;
    }
    lightningWarningShown = false;
}

function setActiveWish(jobId, powerMode) {
    activeWish = {
        jobId,
        powerMode,
        cancelled: false,
        startedAt: Date.now()
    };
    if (powerMode === 'lightning') {
        startLightningWatchdog();
    } else {
        clearLightningWatchdog();
    }
    hideProgressWarning();
    const cancelBtn = document.getElementById('cancel-wish-btn');
    if (cancelBtn) {
        cancelBtn.disabled = false;
    }
}

function clearActiveWish() {
    activeWish = null;
    clearLightningWatchdog();
    hideProgressWarning();
    const cancelBtn = document.getElementById('cancel-wish-btn');
    if (cancelBtn) {
        cancelBtn.disabled = true;
    }
}

function cancelActiveWish() {
    if (!activeWish || activeWish.cancelled) return;
    activeWish.cancelled = true;
    Soundboard.unlock();
    playSound('error');
    updateProgressWarning('Cancelling wish... Awaiting confirmation from SHENRON.', 'info');
    const cancelBtn = document.getElementById('cancel-wish-btn');
    if (cancelBtn) {
        cancelBtn.disabled = true;
    }
    if (agentModeEnabled && agentConsoleVisible) {
        logToConsole('🛑 Wish cancellation requested by user.', 'warning');
    }
    if (activeWish.jobId) {
        fetch(API_BASE, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: 'cancel_wish', job_id: activeWish.jobId })
        })
        .then(res => res.json().catch(() => ({})))
        .then(data => {
            if (!data || data.success !== true) {
                console.warn('⚠️ Cancellation request not acknowledged', data);
                updateProgressWarning('Cancellation requested, awaiting server confirmation...', 'info');
            } else {
                console.log('🛑 Cancellation acknowledged by server', data);
                updateProgressWarning('Cancellation acknowledged. Finalizing...', 'info');
            }
        })
        .catch(err => {
            console.error('❌ Failed to request cancellation', err);
            updateProgressWarning('Cancellation requested locally. Waiting for server response...', 'info');
        });
    }
}

function showShenronOverlay() {
    const overlay = document.getElementById('shenron-overlay');
    if (!overlay || overlay.classList.contains('active')) return;
    overlay.classList.add('active');
    overlay.setAttribute('aria-hidden', 'false');
    playSound('shenron-summon');
    if (shenronOverlayTimer) clearTimeout(shenronOverlayTimer);
    shenronOverlayTimer = setTimeout(() => {
        hideShenronOverlay();
    }, 5000);
}

function hideShenronOverlay() {
    const overlay = document.getElementById('shenron-overlay');
    if (!overlay) return;
    overlay.classList.remove('active');
    overlay.setAttribute('aria-hidden', 'true');
    if (shenronOverlayTimer) {
        clearTimeout(shenronOverlayTimer);
        shenronOverlayTimer = null;
    }
}

function formatRemainingTime(seconds) {
    if (seconds === null || seconds === undefined) return '--';
    const clamped = Math.max(0, Math.round(seconds));
    const minutes = Math.floor(clamped / 60);
    const secs = clamped % 60;
    if (minutes > 60) {
        const hours = Math.floor(minutes / 60);
        const remMinutes = minutes % 60;
        return `${hours}h ${remMinutes}m`;
    }
    if (minutes > 0) {
        return `${minutes}m ${secs.toString().padStart(2, '0')}s`;
    }
    return `${secs}s`;
}

// ============================================================================
// LIVE CLOCK & LOCATION
// ============================================================================

function updateClock() {
    const clockEl = document.getElementById('current-time');
    if (!clockEl) return;
    
    const now = new Date();
    
    // Format: "Thu, Nov 6 • 3:45:23 PM EST"
    const options = {
        weekday: 'short',
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        second: '2-digit',
        hour12: true,
        timeZoneName: 'short'
    };
    
    const formatted = now.toLocaleString('en-US', options);
    clockEl.textContent = `📅 ${formatted}`;
}

function getUserLocation() {
    const locationEl = document.getElementById('user-location');
    if (!locationEl) return;
    
    // Try to get user's timezone
    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    
    // Try geolocation API (will ask for permission)
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                // Success: show approximate location
                fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${position.coords.latitude}&lon=${position.coords.longitude}`)
                    .then(res => res.json())
                    .then(data => {
                        const city = data.address.city || data.address.town || data.address.village || '';
                        const state = data.address.state || '';
                        const country = data.address.country_code?.toUpperCase() || '';
                        
                        locationEl.textContent = `📍 ${city}, ${state} ${country}`;
                    })
                    .catch(() => {
                        locationEl.textContent = `📍 ${timezone}`;
                    });
            },
            () => {
                // Permission denied or error: just show timezone
                locationEl.textContent = `📍 ${timezone}`;
            },
            { timeout: 5000, enableHighAccuracy: false }
        );
    } else {
        // Geolocation not available: show timezone
        locationEl.textContent = `📍 ${timezone}`;
    }
}

// ============================================================================
// MAIN SHENRON SUMMONING FUNCTION
// ============================================================================

async function summonShenron() {
    const textarea = document.getElementById('wish-input') || document.getElementById('question');
    const question = textarea.value.trim();
    
    if (!question) {
        alert('📜 State your wish clearly, mortal!');
        return;
    }
    
    resetUI();
    clearActiveWish();
    setRadarActive(true);
    refreshDragonBallStrip();

    Soundboard.unlock();
    playSound('start');
    
    if (agentModeEnabled) {
        showAgentConsole();
        logToConsole('🐉 Summoning SHENRON...', 'info');
        logToConsole(`🛰️ Query: ${question}`, 'debug');
    } else {
        hideAgentConsole();
    }
    
    const summonBtn = document.querySelector('.summon-btn');
    const originalText = summonBtn.innerHTML;
    summonBtn.innerHTML = '🐉 SUMMONING...';
    summonBtn.disabled = true;
    
    // Show progress section and update warrior statuses
    const progressSection = document.getElementById('progress-section');
    if (progressSection) {
        progressSection.classList.remove('hidden');
    }
    
    // Keep council members visible, just update their status
    document.querySelectorAll('.status-bar').forEach(status => {
        if (status.id?.startsWith('status-')) {
            const warriorKey = status.id.replace('status-', '').toLowerCase();
            updateWarriorStatus(warriorKey, 'thinking', 'Consulting...');
        }
    });
    
    const requestStartTime = Date.now();
    
    try {
        const fastModeEnabled = document.getElementById('fast-mode-checkbox')?.checked || false;
        
        if (fastModeEnabled) {
            console.log('⚡ FAST MODE ACTIVATED - Bypassing SHENRON orchestrator');
            setScreenAura('lightning');
            const results = await fastModeQuery(question);
            displayFastModeResults(results);
        } else {
            console.log('🐉 SHENRON MODE - Full orchestration');
            
            // Determine effective power mode
            let effectivePowerMode = 'council'; // default
            if (agentModeEnabled) {
                if (selectedPowerMode === 'auto') {
                    effectivePowerMode = detectPowerMode(question);
                    console.log(`🧠 AUTO-DETECTED Power Mode: ${POWER_MODES[effectivePowerMode].icon} ${POWER_MODES[effectivePowerMode].name}`);
                } else {
                    effectivePowerMode = selectedPowerMode;
                    console.log(`⚡ MANUAL Power Mode: ${POWER_MODES[effectivePowerMode].icon} ${POWER_MODES[effectivePowerMode].name}`);
                }
                
                const modeInfo = POWER_MODES[effectivePowerMode];
                console.log(`   Power: ${modeInfo.power} | Warriors: ${modeInfo.warriors} | Accuracy: ${modeInfo.accuracy} | Time: ${modeInfo.time}`);
                logToConsole(`${modeInfo.icon} Power Mode: ${modeInfo.name}`, 'info');
                logToConsole(`⚙️ Config → Power: ${modeInfo.power} | Warriors: ${modeInfo.warriors} | Accuracy: ${modeInfo.accuracy} | Time: ${modeInfo.time}`, 'debug');
            }
            setScreenAura(effectivePowerMode);
            
            // Use standard API with power mode config
            const data = await callShenronAPI(question, agentModeEnabled, effectivePowerMode);
            const elapsedTime = ((Date.now() - requestStartTime) / 1000).toFixed(2);
            
            // Manually trigger warrior animations based on response times
            if (data.warrior_responses) {
                animateWarriorCompletionsFromStart(data.warrior_responses, requestStartTime);
            }
            
            showResults(data, elapsedTime);
            
            if (agentModeEnabled) {
                logToConsole(`✅ Wish granted in ${elapsedTime}s`, 'success');
            }
        }
        
    } catch (error) {
        console.error('Summoning failed:', error);
        if (error.message === 'Wish cancelled by user.') {
            if (agentModeEnabled) {
                logToConsole('🛑 Summoning cancelled by user request.', 'warning');
            }
            updateProgressWarning('Wish cancelled. No actions executed.', 'info');
            setRadarActive(false);
            setScreenAura(null);
            hideShenronOverlay();
        } else {
            if (agentModeEnabled) {
                logToConsole(`❌ Summoning failed: ${error.message}`, 'error');
            }
            playSound('critical-error');
            setRadarActive(false);
            setScreenAura(null);
            hideShenronOverlay();
            alert('⚡ The summoning has failed! Check console for details.');
        }
    } finally {
        summonBtn.innerHTML = originalText;
        summonBtn.disabled = false;
    }
}

/**
 * Animate warrior statuses turning green based on their response times
 * Simulates real-time by calculating delays from the original start time
 */
function animateWarriorCompletionsFromStart(responses, requestStartTime) {
    const now = Date.now();
    const elapsed = now - requestStartTime;

    responses.forEach(warrior => {
        const key = warrior.fighter.toLowerCase();
        const responseTime = (warrior.response_time || 0) * 1000; // Convert to ms
        
        // Calculate how much time has already passed
        const remainingDelay = Math.max(0, responseTime - elapsed);

        const timeout = setTimeout(() => {
            if (warrior.success) {
                updateWarriorStatus(key, 'done', '✓ Complete', { responseTime: warrior.response_time });
                playSound('warrior-complete');
            } else {
                updateWarriorStatus(key, 'error', '✗ Failed', { responseTime: warrior.response_time });
                playSound('error');
            }
        }, remainingDelay);

        animationTimeouts.push(timeout);
    });
}

function updateWarriorStatus(warriorKey, state, text, options = {}) {
    const statusEl = document.getElementById(`status-${warriorKey}`);
    if (!statusEl) return;
    const previousState = statusEl.dataset.state || 'idle';
    statusEl.dataset.state = state;

    statusEl.classList.remove('idle', 'thinking', 'done', 'error');
    statusEl.classList.add(state);
    statusEl.textContent = text;
    
    logWarriorProgress(warriorKey, state, text);

    const currentRecord = warriorHealthState[warriorKey] || {};
    let responseTime = currentRecord.responseTime ?? null;
    if (typeof options.responseTime === 'number') {
        responseTime = options.responseTime;
    } else if (state === 'idle' || state === 'thinking') {
        responseTime = null;
    }
    warriorHealthState[warriorKey] = {
        state,
        responseTime,
        text,
        updatedAt: Date.now()
    };
    renderWarriorHealthSummary();

    // Update dragon ball strip
    const balls = document.querySelectorAll('.dragon-ball');
    const warriorMapping = ['goku', 'vegeta', 'piccolo', 'gohan', 'krillin', 'frieza'];
    const index = warriorMapping.indexOf(warriorKey);
    if (index !== -1) {
        const ball = balls[index];
        if (state === 'done') {
            ball.classList.add('active');
        } else if (state === 'idle') {
            ball.classList.remove('active');
        }
    }
    if (state === 'done' && previousState !== 'done') {
        triggerRadarPing();
        playSound('warrior-complete');
    } else if (state === 'error' && previousState !== 'error') {
        playSound('error');
    }
    refreshDragonBallStrip();
}

function resetWarriorStatuses() {
    Object.keys(WARRIORS).forEach(key => {
        updateWarriorStatus(key, 'idle', 'Ready');
    });
    refreshDragonBallStrip();
}

function showProgress() {
    const progressSection = document.getElementById('progress-section');
    progressSection.classList.remove('hidden');
    
    const progressFill = document.getElementById('progress-fill');
    progressFill.style.width = '0%';
    
    animateProgress();
}

function animateProgress() {
    const progressFill = document.getElementById('progress-fill');
    const progressText = document.getElementById('progress-text');
    
    let progress = 0;
    const interval = setInterval(() => {
        if (progress < 90) {
            progress += Math.random() * 5;
            progressFill.style.width = `${Math.min(progress, 90)}%`;
            
            if (progress < 30) {
                progressText.textContent = '🐉 SHENRON is searching the knowledge base...';
            } else if (progress < 60) {
                progressText.textContent = '🐉 SHENRON is consulting all 6 warriors...';
            } else {
                progressText.textContent = '🐉 SHENRON is synthesizing the council\'s wisdom...';
            }
        }
    }, 500);
    
    window.currentProgressInterval = interval;
}

function updateProgressStatus(progressValue, statusMessage, metaText) {
    const progressFill = document.getElementById('progress-fill');
    const progressPercentage = document.getElementById('progress-percentage');
    const progressText = document.getElementById('progress-text');
    const progressTime = document.getElementById('progress-time');
    const powerReadout = document.getElementById('metric-power-readout');
    const panel = document.getElementById('metrics-panel');
    const clamped = typeof progressValue === 'number' ? Math.max(0, Math.min(100, progressValue)) : null;

    if (typeof progressValue === 'number' && progressFill && progressPercentage) {
        progressFill.style.width = `${clamped}%`;
        progressPercentage.textContent = `${Math.round(clamped)}%`;
    }

    if (progressText && statusMessage) {
        progressText.textContent = statusMessage;
    }

    if (progressTime) {
        progressTime.textContent = metaText ? metaText : (statusMessage ? `Status: ${statusMessage}` : 'Status: --');
    }

    if (powerReadout) {
        const pseudoLevel = Math.floor((progressValue || 0) * 120);
        if (pseudoLevel > 9000) {
            powerReadout.textContent = 'Power LVL OVER 9000!';
        } else {
            powerReadout.textContent = `Power LVL ${pseudoLevel.toString().padStart(4, '0')}`;
        }
    }

    if (panel) {
        panel.classList.remove('power-lightning', 'power-council', 'power-ultra');
        if (metaText?.includes('LIGHTNING')) {
            panel.classList.add('power-lightning');
        } else if (metaText?.includes('COUNCIL')) {
            panel.classList.add('power-council');
        } else if (metaText?.includes('ULTRA')) {
            panel.classList.add('power-ultra');
        }
        if (clamped !== null) {
            updateRadarSpeed(clamped);
            const active = clamped > 0 && clamped < 100;
            panel.classList.toggle('radar-active', active);
            if (clamped >= 95) {
                triggerPowerBurst();
            }
            if (clamped >= 100) {
                panel.classList.remove('radar-active');
                hideProgressWarning();
            }
        }
    }
}

async function fetchSystemMetrics() {
    const panel = document.getElementById('metrics-panel');
    if (!panel) return;

    try {
        const response = await fetch(API_BASE, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: 'metrics' })
        });

        if (!response.ok) {
            throw new Error(`Metrics HTTP ${response.status}`);
        }

        const data = await response.json();
        updateSystemMetricsUI(data);
    } catch (error) {
        console.error('Metrics fetch failed:', error);
        markMetricsOffline(error);
    }
}

function markMetricsOffline(err) {
    const panel = document.getElementById('metrics-panel');
    if (!panel) return;
    panel.classList.add('offline');
    jobEventKeys.length = 0;

    const placeholders = [
        'metric-cpu',
        'metric-cpu-detail',
        'metric-ram',
        'metric-ram-detail',
        'metric-disk',
        'metric-disk-detail',
        'metric-lm',
        'metric-lm-models',
        'metric-jobs-summary'
    ];
    placeholders.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.textContent = '--';
    });

    const eventsEl = document.getElementById('metric-events');
    if (eventsEl) {
        const reason = err ? (err.message || err.toString()) : 'Unknown error';
        eventsEl.innerHTML = `<div class="metric-event error">⚠️ Metrics unavailable: ${reason}</div>`;
    }

    const updatedEl = document.getElementById('metrics-updated');
    if (updatedEl) {
        updatedEl.textContent = 'Offline';
    }
}

function applyVisualEffectsSetting() {
    const body = document.body;
    if (!body) return;
    if (visualEffectsEnabled) {
        body.classList.remove('visuals-minimal');
    } else {
        body.classList.add('visuals-minimal');
    }
    const toggle = document.getElementById('visual-toggle');
    if (toggle) {
        toggle.classList.toggle('minimal', !visualEffectsEnabled);
        toggle.title = visualEffectsEnabled ? 'Visual effects enabled' : 'Visual effects reduced';
    }
}

function registerVisualToggle(btn) {
    if (!btn || btn.dataset.bound) return;
    btn.dataset.bound = 'true';
    btn.addEventListener('click', () => {
        visualEffectsEnabled = !visualEffectsEnabled;
        localStorage.setItem('dragonRadarVisuals', visualEffectsEnabled ? 'full' : 'minimal');
        applyVisualEffectsSetting();
        playSound('toggle');
    });
    applyVisualEffectsSetting();
}

function updateSystemMetricsUI(data) {
    const panel = document.getElementById('metrics-panel');
    if (!panel) return;

    panel.classList.remove('offline');

    const updatedEl = document.getElementById('metrics-updated');
    if (updatedEl) {
        const ts = data.timestamp ? new Date(data.timestamp * 1000) : new Date();
        updatedEl.textContent = `Updated ${ts.toLocaleTimeString()}`;
    }

    const system = data.system || {};
    const cpuEl = document.getElementById('metric-cpu');
    const cpuDetail = document.getElementById('metric-cpu-detail');
    if (cpuEl) {
        cpuEl.textContent = (typeof system.cpu_percent === 'number')
            ? `${system.cpu_percent.toFixed(1)}%`
            : '--';
    }
    if (cpuDetail) {
        cpuDetail.textContent = system.psutil_available
            ? 'Real-time CPU usage'
            : 'psutil unavailable';
    }

    const ramEl = document.getElementById('metric-ram');
    const ramDetail = document.getElementById('metric-ram-detail');
    if (ramEl) {
        ramEl.textContent = (typeof system.memory_percent === 'number')
            ? `${system.memory_percent.toFixed(1)}%`
            : '--';
    }
    if (ramDetail) {
        ramDetail.textContent = (typeof system.memory_available_mb === 'number')
            ? `${system.memory_available_mb.toLocaleString()} MB free`
            : '--';
    }

    const diskEl = document.getElementById('metric-disk');
    const diskDetail = document.getElementById('metric-disk-detail');
    if (diskEl) {
        diskEl.textContent = (typeof system.disk_percent === 'number')
            ? `${system.disk_percent.toFixed(1)}%`
            : '--';
    }
    if (diskDetail) {
        diskDetail.textContent = (typeof system.disk_free_gb === 'number')
            ? `${system.disk_free_gb.toFixed(1)} GB free`
            : '--';
    }

    const lm = data.lm_studio || {};
    const lmEl = document.getElementById('metric-lm');
    const lmModelsEl = document.getElementById('metric-lm-models');
    if (lmEl) {
        lmEl.textContent = lm.online
            ? `Online (${lm.model_count || 0})`
            : 'Offline';
        if (!lm.online) {
            panel.classList.add('offline');
        }
    }
    if (lmModelsEl) {
        if (lm.online && Array.isArray(lm.models) && lm.models.length) {
            const visibleModels = lm.models.slice(0, 3).join(', ');
            const extra = lm.models.length > 3 ? ` +${lm.models.length - 3}` : '';
            lmModelsEl.textContent = `${visibleModels}${extra}`;
        } else {
            lmModelsEl.textContent = lm.error ? `⚠️ ${lm.error}` : '--';
        }
    }

    const jobs = data.jobs || {};
    const summaryEl = document.getElementById('metric-jobs-summary');
    if (summaryEl) {
        const statusCounts = jobs.status_counts || {};
        const running = statusCounts.running || 0;
        const queued = statusCounts.queued || 0;
        const completed = statusCounts.completed || 0;
        summaryEl.textContent = `Total: ${jobs.total || 0} • Running: ${running} • Queued: ${queued} • Completed: ${completed}`;
    }

    const eventsEl = document.getElementById('metric-events');
    if (eventsEl) {
        const rawEvents = Array.isArray(data.recent_events) ? data.recent_events : [];

        if (!rawEvents.length && !jobEventKeys.length) {
            eventsEl.innerHTML = '<div class="metric-event">No recent activity</div>';
        } else {
            const fragment = document.createDocumentFragment();
            const eventsAscending = rawEvents.slice().reverse();

            eventsAscending.forEach(event => {
                const timeKey = typeof event.timestamp === 'number' ? event.timestamp : Date.now();
                const jobFragment = event.job_id ? event.job_id : 'unknown';
                const messageFragment = event.message || '';
                const key = `${timeKey}-${jobFragment}-${messageFragment}`;

                if (jobEventKeys.includes(key)) {
                    return;
                }

                jobEventKeys.push(key);

                const type = event.type || 'info';
                const time = event.timestamp ? new Date(event.timestamp * 1000).toLocaleTimeString() : '--';
                const jobLabel = event.job_id ? `<span class="event-job">${event.job_id.slice(0, 6)}</span>` : '';
                const message = messageFragment;

                const wrapper = document.createElement('div');
                wrapper.className = `metric-event ${type}`;
                wrapper.innerHTML = `${jobLabel} <span class="event-time">${time}</span> ${message}`;
                fragment.appendChild(wrapper);
            });

            if (fragment.children.length) {
                if (eventsEl.textContent === 'No recent activity') {
                    eventsEl.innerHTML = '';
                }
                eventsEl.appendChild(fragment);

                if (jobEventKeys.length > jobEventMax) {
                    while (jobEventKeys.length > jobEventMax && eventsEl.firstChild) {
                        jobEventKeys.shift();
                        eventsEl.removeChild(eventsEl.firstChild);
                    }
                }

                eventsEl.scrollTop = eventsEl.scrollHeight;
            }
        }
    }
}

function hideProgress() {
    const progressSection = document.getElementById('progress-section');
    progressSection.classList.add('hidden');
    
    if (window.currentProgressInterval) {
        clearInterval(window.currentProgressInterval);
    }
    
    const progressFill = document.getElementById('progress-fill');
    progressFill.style.width = '100%';
}

function showResults(data, elapsedTime) {
    // Show results section (keep council members visible with "Complete" status)
    const resultsSection = document.getElementById('shenron-response-section');
    if (resultsSection) resultsSection.classList.remove('hidden');
    
    // Update progress to 100%
    const progressFill = document.getElementById('progress-fill');
    const progressPercentage = document.getElementById('progress-percentage');
    if (progressFill) progressFill.style.width = '100%';
    if (progressPercentage) progressPercentage.textContent = '100%';

    // SHENRON's unified response
    const shenronBox = document.getElementById('shenron-synthesis');
    if (!shenronBox) {
        console.error('shenron-synthesis element not found!');
        return;
    }
    
    const consensusBadge = getConsensusBadge(data.consensus);
    
    const ragIndicator = data.rag_used ? '📚 RAG: Yes' : '📚 RAG: No';
    const synthesisMethod = data.synthesis_method === 'true_ai' ? '🔮 TRUE Synthesis' : '';
    
    shenronBox.innerHTML = `
        <h2>🐉 SHENRON'S UNIFIED RESPONSE 🐉</h2>
        ${consensusBadge}
        <div class="meta-info">⏱️ ${elapsedTime}s • ${ragIndicator} ${synthesisMethod}</div>
        
        <div class="shenron-voice">
            <p class="easter-egg">🐉 <em>So be it, Your Wish Has Been Granted</em> ⚡</p>
            <p class="response-text">${data.synthesized_answer || 'No response received.'}</p>
        </div>
    `;

    // Individual warrior responses
    const individualSection = document.getElementById('warriors-responses');
    if (individualSection && data.warrior_responses) {
        let responsesHTML = '<h3>Individual Warrior Responses:</h3>';
        data.warrior_responses.forEach(warrior => {
            if (!warrior.success) return;
            responsesHTML += `
                <div class="warrior-response">
                    <h4>${warrior.emoji} ${warrior.fighter.toUpperCase()}</h4>
                    <p>${warrior.answer}</p>
                    <div class="meta">⏱️ ${warrior.response_time.toFixed(2)}s</div>
                </div>
            `;
        });
        individualSection.innerHTML = responsesHTML;
    }

    // Show expand button
    const expandBtn = document.getElementById('expand-warriors-btn');
    if (expandBtn) {
        expandBtn.style.display = 'block';
        expandBtn.onclick = () => {
            if (individualSection) {
                individualSection.classList.toggle('hidden');
                expandBtn.textContent = individualSection.classList.contains('hidden')
                    ? 'View Individual Warrior Responses'
                    : 'Hide Individual Warrior Responses';
            }
        };
    }
    
    // Animate warrior completion statuses
    if (data.warrior_responses && Array.isArray(data.warrior_responses)) {
        animateWarriorCompletionsFromStart(data.warrior_responses, elapsedTime);
    }
    setRadarActive(false);
    setScreenAura(null);
}
function getConsensusBadge(consensus) {
    const types = {
        'unanimous': { class: 'unanimous', text: 'UNANIMOUS', subtitle: 'All 6 warriors agree.' },
        'strong': { class: 'strong', text: 'STRONG', subtitle: consensus.message },
        'majority': { class: 'majority', text: 'MAJORITY', subtitle: consensus.message },
        'weak': { class: 'weak', text: 'WEAK', subtitle: consensus.message },
        'failure': { class: 'error', text: 'FAILED', subtitle: 'No warriors responded.' }
    };

    const badge = types[consensus.type] || types['weak'];
    
    return `
        <div class="consensus-badge ${badge.class}">
            <div class="badge-title">${badge.text}</div>
            <div class="badge-subtitle">${badge.subtitle}</div>
        </div>
    `;
}

function getWishGrantedMessage() {
    return '<div class="wish-granted-message">✨ So be it. Your wish has been granted! ✨</div>';
}

function getWishFailedMessage() {
    return `
        <div class="wish-failed-message">
            ⚡ Your wish cannot be granted because the Guardian of Earth created me. 
            I cannot grant a wish that exceeds His power. ⚡
        </div>
    `;
}

function createUnifiedResponse(data) {
    // Fallback if synthesis fails - show summary
    const successful = data.individual_responses.filter(r => r.success);
    
    if (successful.length === 0) {
        return "The council was unable to provide guidance on this matter.";
    }

    if (successful.length === 1) {
        return successful[0].answer;
    }

    // Simple summary for fallback
    return `Based on the council's deliberation:\n\n${successful[0].answer.substring(0, 500)}...\n\n(See individual warrior insights below for complete responses)`;
}

function createIndividualResponsesHTML(responses) {
    let html = '<h3>📋 View Individual DBZ-Warrior Insights:</h3>';
    
    responses.forEach(warrior => {
        const status = warrior.success ? '✅' : '❌';
        const timeInfo = warrior.success ? `${warrior.response_time.toFixed(1)}s` : 'Failed';
        
        html += `
            <div class="fighter-response ${warrior.success ? '' : 'error'}">
                <div class="fighter-header" onclick="toggleFighterResponse('${warrior.fighter}')">
                    <span class="fighter-title">${warrior.emoji} ${warrior.fighter} (${warrior.role})</span>
                    <span class="fighter-meta">${status} • ${timeInfo} • Model: ${warrior.model}</span>
                </div>
                <div class="fighter-content" id="response-${warrior.fighter}" style="display: none;">
                    ${formatResponse(warrior.answer)}
                </div>
            </div>
        `;
    });
    
    return html;
}

function toggleFighterResponse(fighter) {
    const content = document.getElementById(`response-${fighter}`);
    if (content.style.display === 'none') {
        content.style.display = 'block';
    } else {
        content.style.display = 'none';
    }
}

function formatResponse(text) {
    // Convert markdown-style formatting
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>');
}

function showError(message) {
    document.getElementById('council-members').classList.add('hidden');
    const resultsSection = document.querySelector('.shenron-response-section');
    if (resultsSection) resultsSection.classList.remove('hidden');
    
    const shenronBox = document.getElementById('shenron-synthesis');
    if (shenronBox) {
        shenronBox.innerHTML = `
            <h2>⚡ ERROR ⚡</h2>
            <div class="wish-failed-message">
                ${message}
            </div>
        `;
    }
}

function resetUI() {
    const resultsSection = document.querySelector('.shenron-response-section');
    const councilMembers = document.getElementById('council-members');
    const individualResponses = document.getElementById('warriors-responses');
    
    if (resultsSection) resultsSection.classList.add('hidden');
    if (councilMembers) councilMembers.classList.remove('hidden');
    if (individualResponses) individualResponses.innerHTML = '';
    shenronUnlocked = false;
    setRadarActive(false);
    setScreenAura(null);
    hideShenronOverlay();
    refreshDragonBallStrip();
    resetWarriorStatuses();
}
// ============================================================================
// POWER MODE AUTO-DETECTION & SELECTION
// ============================================================================

function detectPowerMode(query) {
    /**
     * Auto-detect appropriate power mode based on query complexity
     * Returns: 'lightning', 'council', or 'ultra'
     */
    const queryLower = query.toLowerCase();
    const wordCount = query.split(/\s+/).length;
    
    // ULTRA INSTINCT MODE triggers
    const ultraKeywords = [
        'optimize entire', 'analyze all', 'fix everything', 'diagnose and fix',
        'design and deploy', 'autonomous', 'make it perfect', 'best possible',
        'maximum accuracy', 'full analysis', 'complete solution'
    ];
    const complexOperation = wordCount > 50 || (queryLower.includes(' and ') && queryLower.includes(' then '));
    
    if (ultraKeywords.some(kw => queryLower.includes(kw)) || complexOperation) {
        return 'ultra';
    }
    
    // LIGHTNING MODE triggers
    const lightningKeywords = [
        'quick', 'fast', 'what is', 'simple', 'restart', 'status',
        'show me', 'list', 'check', 'tell me', 'what are'
    ];
    const simpleQuery = wordCount < 10;
    
    if (lightningKeywords.some(kw => queryLower.includes(kw)) || simpleQuery) {
        return 'lightning';
    }
    
    // Default: COUNCIL MODE
    return 'council';
}

function updateDetectedModeDisplay(mode) {
    /**
     * Update the UI to show the auto-detected power mode
     */
    const modeInfo = POWER_MODES[mode];
    const detectedModeEl = document.getElementById('auto-detected-mode');
    const detectedInfoEl = document.getElementById('detected-mode-info');
    
    if (!detectedModeEl || !detectedInfoEl) return;
    
    // Only show if AUTO mode is selected
    const autoSelected = document.querySelector('input[name="power-mode"]:checked')?.value === 'auto';
    
    if (autoSelected) {
        detectedModeEl.classList.remove('hidden');
        detectedInfoEl.innerHTML = `
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 16px;">${modeInfo.icon}</span>
                <div>
                    <div style="font-weight: bold; color: ${modeInfo.color};">${modeInfo.name}</div>
                    <div style="font-size: 10px; color: #95a5a6;">
                        Power: ${modeInfo.power} • ${modeInfo.warriors} Warrior${modeInfo.warriors > 1 ? 's' : ''} • Time: ${modeInfo.time} • Accuracy: ${modeInfo.accuracy}
                    </div>
                </div>
            </div>
        `;
    } else {
        detectedModeEl.classList.add('hidden');
    }
}

function initializePowerModeListeners() {
    /**
     * Set up all Power Mode event listeners
     */
    
    // Listen to query input for auto-detection
    const wishInput = document.getElementById('wish-input') || document.getElementById('question');
    if (wishInput) {
        wishInput.addEventListener('input', (e) => {
            if (agentModeEnabled && e.target.value.trim()) {
                detectedPowerMode = detectPowerMode(e.target.value);
                updateDetectedModeDisplay(detectedPowerMode);
            }
        });
    }
    
    // Listen to power mode radio buttons
    document.querySelectorAll('input[name="power-mode"]').forEach(radio => {
        radio.addEventListener('change', (e) => {
            selectedPowerMode = e.target.value;
            console.log(`⚡ Power Mode changed to: ${selectedPowerMode.toUpperCase()}`);
            
            // Update display if in auto mode
            if (selectedPowerMode === 'auto' && wishInput?.value.trim()) {
                updateDetectedModeDisplay(detectedPowerMode);
            } else {
                document.getElementById('auto-detected-mode')?.classList.add('hidden');
            }
        });
    });
    
    // Agent Mode checkbox toggle
    const agentCheckbox = document.getElementById('agent-mode-checkbox');
    const powerModeSelection = document.getElementById('power-mode-selection');
    const agentModeStatus = document.getElementById('agent-mode-status');
    
    if (agentCheckbox) {
        agentCheckbox.addEventListener('change', async (e) => {
            if (e.target.checked) {
                // Enabling Agent Mode - request 2FA
                const code = prompt('🔐 Enter your Google Authenticator 6-digit code to enable Agent Mode:');
                
                if (!code || code.length !== 6 || !/^\d{6}$/.test(code)) {
                    e.target.checked = false;
                    alert('❌ Invalid code format. Must be 6 digits.');
                    return;
                }
                
                // Show verifying status
                if (agentModeStatus) agentModeStatus.textContent = 'Verifying...';
                
                // Verify 2FA
                try {
                    const response = await fetch('/verify_2fa.php', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({code: code})
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        agentModeEnabled = true;
                        agentModeVerified = true;
                        agentMode2FAExpires = Date.now() + (60 * 60 * 1000); // 1 hour
                        
                        // Show power mode selection
                        if (powerModeSelection) powerModeSelection.classList.remove('hidden');
                        if (agentModeStatus) {
                            agentModeStatus.textContent = '✅ Enabled (59min remaining)';
                            agentModeStatus.style.color = '#2ecc71';
                        }
                        
                        console.log('🤖✅ Agent Mode ENABLED with 2FA');
                        showAgentConsole();
                        logToConsole('✅ Agent Mode enabled via 2FA', 'success');
                        
                        // Start countdown timer
                        startAgentModeCountdown();
                        
                    } else {
                        e.target.checked = false;
                        agentModeEnabled = false;
                        agentModeVerified = false;
                        if (powerModeSelection) powerModeSelection.classList.add('hidden');
                        if (agentModeStatus) {
                            agentModeStatus.textContent = 'Disabled';
                            agentModeStatus.style.color = '#aaa';
                        }
                        hideAgentConsole();
                        alert('❌ Invalid 2FA code. Please try again.');
                        console.log('🤖❌ 2FA verification failed');
                    }
                } catch (error) {
                    e.target.checked = false;
                    agentModeEnabled = false;
                    if (agentModeStatus) agentModeStatus.textContent = 'Disabled';
                    hideAgentConsole();
                    alert('❌ Error verifying 2FA. Please try again.');
                    console.error('2FA verification error:', error);
                }
                
            } else {
                // Disabling Agent Mode
                agentModeEnabled = false;
                agentModeVerified = false;
                agentMode2FAExpires = null;
                
                if (powerModeSelection) powerModeSelection.classList.add('hidden');
                if (agentModeStatus) {
                    agentModeStatus.textContent = 'Disabled';
                    agentModeStatus.style.color = '#aaa';
                }
                hideAgentConsole();
                
                console.log('🤖❌ Agent Mode DISABLED');
                logToConsole('🛑 Agent Mode disabled', 'warning');
            }
        });
    }
}

function startAgentModeCountdown() {
    /**
     * Update the remaining time for Agent Mode session
     */
    const updateCountdown = () => {
        if (!agentMode2FAExpires) return;
        
        const remaining = Math.max(0, Math.floor((agentMode2FAExpires - Date.now()) / 1000 / 60));
        const agentModeStatus = document.getElementById('agent-mode-status');
        
        if (remaining > 0) {
            if (agentModeStatus) {
                agentModeStatus.textContent = `✅ Enabled (${remaining}min remaining)`;
            }
        } else {
            // Session expired
            agentModeEnabled = false;
            agentModeVerified = false;
            agentMode2FAExpires = null;
            
            const checkbox = document.getElementById('agent-mode-checkbox');
            if (checkbox) checkbox.checked = false;
            
            if (agentModeStatus) {
                agentModeStatus.textContent = 'Session Expired';
                agentModeStatus.style.color = '#e74c3c';
            }
            
            document.getElementById('power-mode-selection')?.classList.add('hidden');
            alert('⏰ Agent Mode session expired. Please re-authenticate.');
            logToConsole('⏰ Agent Mode session expired. Please re-authenticate.', 'warning');
            hideAgentConsole();
        }
    };
    
    // Update every minute
    setInterval(updateCountdown, 60000);
}

document.addEventListener('DOMContentLoaded', () => {
    initializeWarriorHealthState();

    // Initialize clock
    updateClock();
    setInterval(updateClock, 1000); // Update every second
    
    // Get user location
    getUserLocation();

    const audioToggle = document.getElementById('audio-toggle');
    Soundboard.registerToggle(audioToggle);
    const safeUnlock = () => Soundboard.unlock();
    document.addEventListener('pointerdown', safeUnlock, { once: true, passive: true });
    document.addEventListener('click', safeUnlock, { once: true, passive: true });
    document.addEventListener('keydown', safeUnlock, { once: true, passive: true });

    const visualToggle = document.getElementById('visual-toggle');
    if (visualToggle) {
        registerVisualToggle(visualToggle);
    } else {
        applyVisualEffectsSetting();
    }

    const cancelBtn = document.getElementById('cancel-wish-btn');
    if (cancelBtn) {
        cancelBtn.disabled = true;
        if (!cancelBtn.dataset.bound) {
            cancelBtn.dataset.bound = 'true';
            cancelBtn.addEventListener('click', cancelActiveWish);
        }
    }

    // Initialize system metrics polling
    fetchSystemMetrics();
    if (metricsInterval) {
        clearInterval(metricsInterval);
    }
    metricsInterval = setInterval(fetchSystemMetrics, 10000);
    
    // Initialize Power Mode listeners
    initializePowerModeListeners();
    
    // Initialize summon button
    const summonBtn = document.getElementById('summon-btn');
    if (summonBtn) {
        summonBtn.addEventListener('click', summonShenron);
    }
    
    // Allow Enter key to summon
    const questionEl = document.getElementById('question');
    if (questionEl) {
        questionEl.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                summonShenron();
            }
        });
    }
    
    initAgentConsole();
    console.log('🐉 SHENRON SYNDICATE v3.3 - Initialized');
    console.log('Features: TRUE Synthesis • Agent Mode • RAG • 6 DBZ-Warriors');
    console.log('Easter Egg: Try hovering over the warriors! ⚡');
    refreshDragonBallStrip();
});

// ============================================================================
// LIVE AGENT CONSOLE
// ============================================================================

function initAgentConsole() {
    const consoleEl = document.getElementById('agent-console');
    if (!consoleEl) return;

    const toggleBtn = document.getElementById('console-toggle');
    const clearBtn = document.getElementById('console-clear');

    if (toggleBtn && !toggleBtn.dataset.bound) {
        toggleBtn.dataset.bound = 'true';
        toggleBtn.addEventListener('click', () => {
            consoleMinimized = !consoleMinimized;
            if (consoleMinimized) {
                consoleEl.classList.add('minimized');
                toggleBtn.textContent = '▲ Maximize';
            } else {
                consoleEl.classList.remove('minimized');
                toggleBtn.textContent = '▼ Minimize';
            }
        });
    }

    if (clearBtn && !clearBtn.dataset.bound) {
        clearBtn.dataset.bound = 'true';
        clearBtn.addEventListener('click', () => {
            const output = document.getElementById('console-output');
            if (output) {
                output.innerHTML = '<div class="console-line">🐉 Console cleared...</div>';
            }
        });
    }

    makeConsoleDraggable(consoleEl);

    if (!window.__agentConsolePatched) {
        const originalConsoleLog = console.log.bind(console);
        console.log = function (...args) {
            originalConsoleLog(...args);

            if (agentModeEnabled && agentConsoleVisible) {
                const message = args.map(arg =>
                    typeof arg === 'object' ? JSON.stringify(arg, null, 2) : String(arg)
                ).join(' ');

                let type = 'info';
                if (message.includes('✅') || message.includes('SUCCESS') || message.includes('Complete')) {
                    type = 'success';
                } else if (message.includes('⚠️') || message.includes('WARNING')) {
                    type = 'warning';
                } else if (message.includes('❌') || message.includes('ERROR') || message.includes('Failed')) {
                    type = 'error';
                } else if (message.includes('🔍') || message.includes('DEBUG')) {
                    type = 'debug';
                }

                logToConsole(message, type);
            }
        };

        window.__agentConsolePatched = true;
    }
}

function makeConsoleDraggable(consoleEl) {
    const header = consoleEl?.querySelector('.console-header');
    if (!consoleEl || !header) return;

    let isDragging = false;
    let initialX;
    let initialY;

    header.addEventListener('mousedown', (e) => {
        if (e.target.tagName === 'BUTTON') return;
        isDragging = true;
        initialX = e.clientX - consoleEl.offsetLeft;
        initialY = e.clientY - consoleEl.offsetTop;
        consoleEl.classList.add('dragging');
    });

    document.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        e.preventDefault();
        const currentX = e.clientX - initialX;
        const currentY = e.clientY - initialY;
        consoleEl.style.left = `${currentX}px`;
        consoleEl.style.top = `${currentY}px`;
        consoleEl.style.bottom = 'auto';
        consoleEl.style.right = 'auto';
    });

    document.addEventListener('mouseup', () => {
        if (!isDragging) return;
        isDragging = false;
        consoleEl.classList.remove('dragging');
    });
}

function showAgentConsole() {
    const consoleEl = document.getElementById('agent-console');
    if (!consoleEl) return;
    consoleEl.classList.remove('hidden');
    consoleEl.classList.add('scouter-active');
    agentConsoleVisible = true;
}

function hideAgentConsole() {
    const consoleEl = document.getElementById('agent-console');
    if (!consoleEl) return;
    consoleEl.classList.add('hidden');
    consoleEl.classList.remove('scouter-active');
    agentConsoleVisible = false;
}

function logToConsole(message, type = 'info') {
    const output = document.getElementById('console-output');
    if (!output) return;

    const timestamp = new Date().toLocaleTimeString('en-US', {
        hour12: false,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });

    const line = document.createElement('div');
    line.className = `console-line ${type}`;
    line.innerHTML = `<span class="timestamp">[${timestamp}]</span>${message}`;
    output.appendChild(line);
    output.scrollTop = output.scrollHeight;

    while (output.children.length > 150) {
        output.removeChild(output.firstChild);
    }
}

function logWarriorProgress(warriorKey, state, text) {
    if (!agentModeEnabled || !agentConsoleVisible) return;
    const warrior = WARRIORS[warriorKey];
    if (!warrior) return;

    let type = 'info';
    if (state === 'done' || state === 'complete') {
        type = 'success';
    } else if (state === 'error' || state === 'failed') {
        type = 'error';
    } else if (state === 'thinking' || state === 'consulting') {
        type = 'info';
    }

    logToConsole(`${warrior.emoji} ${warrior.name}: ${text}`, type);
}

// ============================================================================
// AGENT MODE v4.1 - Enhancement for SHENRON Syndicate
// Add this to the end of script.js
// ============================================================================

// Agent Mode Execution Log
const agentExecutionLog = [];

// Initialize Agent Mode on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeAgentMode();
});

function initializeAgentMode() {
    const agentModeCheckbox = document.getElementById('agentMode');
    const agentModeInfo = document.getElementById('agentModeInfo');
    const agentModeStatus = document.getElementById('agentModeStatus');
    
    if (!agentModeCheckbox) return;
    
    // Load saved state from localStorage
    const saved = localStorage.getItem('agentModeEnabled');
    if (saved === 'true') {
        agentModeCheckbox.checked = true;
        agentModeEnabled = true;
        agentModeInfo.classList.remove('hidden');
        agentModeStatus.textContent = '(Active - Command Execution Enabled)';
    }
    
    // Toggle handler
    agentModeCheckbox.addEventListener('change', (e) => {
        agentModeEnabled = e.target.checked;
        localStorage.setItem('agentModeEnabled', agentModeEnabled);
        
        if (agentModeEnabled) {
            agentModeInfo.classList.remove('hidden');
            agentModeStatus.textContent = '(Active - Command Execution Enabled)';
            console.log('🤖 Agent Mode ENABLED');
        } else {
            agentModeInfo.classList.add('hidden');
            agentModeStatus.textContent = '(Command Execution)';
            console.log('🤖 Agent Mode DISABLED');
        }
    });
    
    console.log('Features: TRUE Synthesis • Agent Mode v4.1 • RAG • 6 DBZ-Warriors');
}

// Enhanced summonShenron function (replaces original)
async function summonShenronWithAgentMode() {
    Soundboard.unlock();
    const questionEl = document.getElementById('question');
    const question = questionEl.value.trim();

    if (!question) {
        alert('📜 State your wish clearly, mortal!');
        return;
    }

    // Detect if query contains command-like phrases
    const commandKeywords = ['check', 'restart', 'status', 'disk space', 'run', 'execute', 'show logs'];
    const possiblyHasCommand = commandKeywords.some(keyword => 
        question.toLowerCase().includes(keyword)
    );

    if (agentModeEnabled && possiblyHasCommand) {
        console.log('🤖 Agent Mode: Query may contain command requests');
    }

    // Call original summonShenron logic
    // (The existing summonShenron function will handle the API call)
    
    // Pass agent_mode flag if enabled
    return await callShenronAPI(question, agentModeEnabled);
}

// API call with STREAMING support for real-time warrior updates
async function callShenronAPIStreaming(query, agentMode = false) {
    console.log('🐉 Starting streaming API call...');
    
    return new Promise((resolve, reject) => {
        const requestBody = {
            query: query,
            agent_mode: agentMode,
            stream: true  // Tell backend we want streaming
        };
        
        fetch(API_BASE, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'text/event-stream'
            },
            body: JSON.stringify(requestBody)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';
            let finalResult = null;
            let warriorCount = 0;
            const totalWarriors = 6;
            
            function processLine(line) {
                if (line.startsWith('data: ')) {
                    try {
                        const data = JSON.parse(line.substring(6));
                        
                        switch (data.type) {
                            case 'warrior_complete':
                                warriorCount++;
                                const warrior = data.warrior;
                                console.log(`✅ ${warrior.emoji} ${warrior.fighter} completed (${warrior.response_time.toFixed(1)}s)`);
                                
                                // UPDATE UI IMMEDIATELY! Turn warrior green
                                updateWarriorStatus(warrior.fighter.toLowerCase(), 'done', `Complete (${warrior.response_time.toFixed(1)}s)`);
                                
                                // Update progress dynamically based on actual warriors completing
                                const progress = Math.floor((warriorCount / totalWarriors) * 85); // 0-85% for warriors
                                const progressFill = document.getElementById('progress-fill');
                                const progressPercentage = document.getElementById('progress-percentage');
                                const progressTime = document.getElementById('progress-time');
                                
                                if (progressFill) progressFill.style.width = progress + '%';
                                if (progressPercentage) progressPercentage.textContent = progress + '%';
                                if (progressTime) progressTime.textContent = `Warriors: ${warriorCount}/${totalWarriors} complete`;
                                break;
                            
                            case 'consensus_start':
                                const pf2 = document.getElementById('progress-fill');
                                const pp2 = document.getElementById('progress-percentage');
                                const pt2 = document.getElementById('progress-time');
                                if (pf2) pf2.style.width = '90%';
                                if (pp2) pp2.textContent = '90%';
                                if (pt2) pt2.textContent = 'Analyzing consensus...';
                                break;
                            
                            case 'synthesis_start':
                                const pf3 = document.getElementById('progress-fill');
                                const pp3 = document.getElementById('progress-percentage');
                                const pt3 = document.getElementById('progress-time');
                                if (pf3) pf3.style.width = '95%';
                                if (pp3) pp3.textContent = '95%';
                                if (pt3) pt3.textContent = 'Synthesizing response...';
                                break;
                            
                            case 'complete':
                                console.log('✅ SHENRON has granted your wish!');
                                finalResult = data;
                                break;
                            
                            case 'error':
                                console.error('❌ Error:', data.error);
                                reject(new Error(data.error));
                                break;
                        }
                    } catch (e) {
                        console.error('Failed to parse SSE data:', line, e);
                    }
                }
            }
            
            function readStream() {
                reader.read().then(({ done, value }) => {
                    if (done) {
                        if (finalResult) {
                            resolve(finalResult);
                        } else {
                            reject(new Error('Stream ended without final result'));
                        }
                        return;
                    }
                    
                    buffer += decoder.decode(value, { stream: true });
                    const lines = buffer.split('\n');
                    buffer = lines.pop();
                    
                    lines.forEach(processLine);
                    readStream();
                }).catch(reject);
            }
            
            readStream();
        })
        .catch(reject);
    });
}

// API call with async job polling (prevents Cloudflare 524 timeouts)
async function callShenronAPI(query, agentMode = false, powerMode = 'council') {
    console.log('🔍 callShenronAPI invoked', { snippet: query.slice(0, 60), agentMode, powerMode });

    const requestBody = {
        action: 'start_wish',
        query,
        power_mode: powerMode,
        agent_mode: agentMode
    };

    const startResponse = await fetch(API_BASE, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
    });

    if (!startResponse.ok) {
        const text = await startResponse.text();
        console.error('🔴 Failed to queue wish', startResponse.status, text);
        throw new Error(`Unable to queue wish (HTTP ${startResponse.status})`);
    }

    const startData = await startResponse.json();
    if (!startData.job_id) {
        console.error('🔴 Unexpected response from start_wish', startData);
        throw new Error(startData.error || 'Failed to start wish job');
    }

    const jobId = startData.job_id;
    console.log('🧾 Wish job queued', { jobId, status: startData.status });

    setActiveWish(jobId, powerMode);

    updateProgressStatus(5, '🐉 Wish queued for SHENRON...', `Job ID: ${jobId}`);
    if (agentMode && agentConsoleVisible) {
        logToConsole(`🧾 Job ${jobId} queued`, 'debug');
        logToConsole('⏳ Awaiting SHENRON council...', 'info');
    }

    const timeouts = {
        ultra: 30 * 60 * 1000,
        council: 5 * 60 * 1000,
        lightning: 2 * 60 * 1000
    };
    const timeoutDuration = timeouts[powerMode] || timeouts.council;
    const pollInterval = powerMode === 'lightning' ? 1500 : 3000;
    const timeoutDeadline = Date.now() + timeoutDuration;
    const startTime = Date.now();

    let lastMessage = null;
    let pollAttempts = 0;
    let lastEventCount = 0;

    while (Date.now() < timeoutDeadline) {
        if (activeWish?.cancelled) {
            clearActiveWish();
            throw new Error('Wish cancelled by user.');
        }

        await sleep(pollInterval);
        pollAttempts += 1;

        if (activeWish?.cancelled) {
            clearActiveWish();
            throw new Error('Wish cancelled by user.');
        }

        const statusResponse = await fetch(API_BASE, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: 'wish_status', job_id: jobId })
        });

        if (statusResponse.status === 404) {
            console.warn('⚠️ Job not found yet, retrying...', { jobId, pollAttempts });
            if (pollAttempts <= 3) {
                continue;
            }
            clearActiveWish();
            throw new Error('Job not found. Please try again.');
        }

        if (!statusResponse.ok) {
            const text = await statusResponse.text();
            console.error('🔴 Failed to fetch job status', statusResponse.status, text);
            clearActiveWish();
            throw new Error(`Unable to fetch job status (HTTP ${statusResponse.status})`);
        }

        const statusData = await statusResponse.json();
        const status = statusData.status || 'unknown';
        const message = statusData.message || `Status: ${status.toUpperCase()}`;
        const backendProgress = typeof statusData.progress === 'number' ? statusData.progress : null;

        const events = Array.isArray(statusData.events) ? statusData.events : [];
        if (events.length > lastEventCount) {
            for (let i = lastEventCount; i < events.length; i++) {
                const event = events[i];
                const eventTime = event.timestamp ? new Date(event.timestamp * 1000).toLocaleTimeString() : '';
                const eventMessage = eventTime ? `[${eventTime}] ${event.message}` : event.message;
                const typeMap = {
                    success: 'success',
                    error: 'error',
                    warning: 'warning',
                    info: 'info'
                };
                const logType = typeMap[event.type] || 'info';
                if (agentMode && agentConsoleVisible) {
                    logToConsole(eventMessage, logType);
                } else {
                    console.log(eventMessage);
                }
            }
            lastEventCount = events.length;
        }

        let progressValue = backendProgress;
        if (progressValue === null) {
            const elapsedRatio = Math.min(1, (Date.now() - startTime) / timeoutDuration);
            progressValue = 5 + (elapsedRatio * 90);
            if (status === 'queued') {
                progressValue = Math.min(progressValue, 20);
            } else if (status === 'running') {
                progressValue = Math.min(progressValue, 95);
            }
        }

        let metaParts = [];
        if (statusData.power_mode) {
            metaParts.push(`Mode: ${statusData.power_mode}`);
        } else {
            metaParts.push(`Job: ${jobId}`);
        }
        if (typeof statusData.estimated_remaining === 'number') {
            metaParts.push(`ETA: ${formatRemainingTime(statusData.estimated_remaining)}`);
        }
        if (typeof statusData.elapsed_seconds === 'number') {
            metaParts.push(`Elapsed: ${formatRemainingTime(statusData.elapsed_seconds)}`);
        }

        updateProgressStatus(progressValue, message, metaParts.join(' • '));

        if (agentMode && agentConsoleVisible && message !== lastMessage) {
            const logType = status === 'failed' ? 'error' : (status === 'completed' ? 'success' : 'info');
            logToConsole(message, logType);
            lastMessage = message;
        }

        if (status === 'completed' && statusData.result) {
            console.log('✅ Wish job completed', { jobId, pollAttempts, duration: (Date.now() - startTime) / 1000 });
            const completionMeta = metaParts.join(' • ') || `Job: ${jobId}`;
            updateProgressStatus(100, '🐉 Wish granted', completionMeta);
            hideProgressWarning();
            if (agentMode && agentConsoleVisible) {
                logToConsole('✅ SHENRON completed the wish', 'success');
            }
            if (agentMode && statusData.result.commands_executed) {
                displayAgentExecutions(statusData.result.commands_executed);
            }
            playSound('all-complete');
            setRadarActive(false);
            clearActiveWish();
            return statusData.result;
        }

        if (status === 'action_required') {
            console.log('⚠️ Wish requires follow-up actions', { jobId, pending: statusData.pending_actions });
            const pending = Array.isArray(statusData.pending_actions) ? statusData.pending_actions : [];
            const followUpMeta = metaParts.join(' • ') || `Job: ${jobId}`;
            updateProgressStatus(progressValue || 95, '⚠️ Additional follow-up required', followUpMeta);
            setRadarActive(false);
            setScreenAura(null);
            hideShenronOverlay();
            showPendingActions(pending);
            if (agentMode && agentConsoleVisible) {
                logToConsole('⚠️ Follow-up actions required:', 'warning');
                pending.forEach((action, idx) => {
                    const summary = action?.summary || action?.status || 'Follow-up required';
                    logToConsole(`${idx + 1}. ${(action?.source || 'Warrior')}: ${summary}`, 'info');
                });
            }
            clearActiveWish();
            return statusData.result || { pending_actions: pending };
        }

        if (status === 'failed') {
            const error = statusData.error || 'SHENRON failed to grant the wish.';
            console.error('🔴 Wish job failed', { jobId, error });
            const failureMeta = metaParts.join(' • ') || `Job: ${jobId}`;
            updateProgressStatus(progressValue || 100, `❌ ${error}`, failureMeta);
            hideProgressWarning();
            setRadarActive(false);
            setScreenAura(null);
            hideShenronOverlay();
            clearActiveWish();
            throw new Error(error);
        }

        if (status === 'cancelled') {
            console.log('🛑 Wish job cancelled', { jobId, pollAttempts, duration: (Date.now() - startTime) / 1000 });
            const cancelMeta = metaParts.join(' • ') || `Job: ${jobId}`;
            updateProgressStatus(progressValue || 0, '🛑 Wish cancelled', cancelMeta);
            hideProgressWarning();
            setRadarActive(false);
            setScreenAura(null);
            hideShenronOverlay();
            clearActiveWish();
            throw new Error('Wish cancelled.');
        }
    }

    console.error('🔴 Wish job timed out', { jobId, timeoutMinutes: timeoutDuration / 60000 });
    clearActiveWish();
    throw new Error('Request timed out. SHENRON may still be processing your wish.');
}
function displayAgentExecutions(commands) {
    const logSection = document.getElementById('agent-log-section');
    const logContainer = document.getElementById('agent-log');
    
    if (!logSection || !logContainer || !commands || commands.length === 0) {
        return;
    }
    
    logSection.classList.remove('hidden');
    
    commands.forEach(cmd => {
        const entry = createLogEntry(cmd);
        logContainer.insertBefore(entry, logContainer.firstChild);
        agentExecutionLog.push(cmd);
        
        if (agentModeEnabled && agentConsoleVisible) {
            const typeMapping = {
                safe: 'info',
                moderate: 'warning',
                dangerous: 'error'
            };
            const logType = typeMapping[cmd.classification] || 'info';
            const host = cmd.host || 'Unknown';
            const commandText = cmd.command || '';
            const outcome = cmd.executed ? (cmd.result || 'Executed successfully') : (cmd.reason || 'Not executed');
            
            logToConsole(`💻 ${host}: ${commandText}`, logType);
            logToConsole(cmd.executed ? `✅ Result: ${outcome}` : `⚠️ Result: ${outcome}`, cmd.executed ? 'success' : 'warning');
        }
    });
}

// Create log entry HTML
function createLogEntry(command) {
    const entry = document.createElement('div');
    entry.className = `agent-log-entry ${command.classification || 'safe'}`;
    
    const timestamp = new Date().toLocaleTimeString();
    
    entry.innerHTML = `
        <div class="log-timestamp">${timestamp}</div>
        <div>
            <span class="log-classification ${command.classification || 'safe'}">${command.classification || 'SAFE'}</span>
            <strong>${command.host || 'Unknown'}</strong>
        </div>
        <div class="log-command">${escapeHtml(command.command)}</div>
        ${command.executed ? 
            `<div class="log-result">✅ ${escapeHtml(command.result || 'Executed successfully')}</div>` :
            `<div class="log-result">⚠️ ${escapeHtml(command.reason || 'Not executed')}</div>`
        }
    `;
    
    return entry;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Show approval dialog for moderate commands
function showApprovalDialog(command, host, callback) {
    // Create overlay
    const overlay = document.createElement('div');
    overlay.className = 'dialog-overlay';
    
    // Create dialog
    const dialog = document.createElement('div');
    dialog.className = 'approval-dialog';
    
    dialog.innerHTML = `
        <h3>⚠️ Command Approval Required</h3>
        <p>SHENRON wants to execute a <strong>MODERATE</strong> command:</p>
        <div class="command-preview">${escapeHtml(command)}</div>
        <p><strong>Host:</strong> ${escapeHtml(host)}</p>
        <p class="warning-text">This command will restart a service. Do you approve?</p>
        <div class="approval-dialog-buttons">
            <button class="approve-btn" id="approve-btn">✅ Approve & Execute</button>
            <button class="deny-btn" id="deny-btn">❌ Deny</button>
        </div>
    `;
    
    document.body.appendChild(overlay);
    document.body.appendChild(dialog);
    
    // Button handlers
    document.getElementById('approve-btn').addEventListener('click', () => {
        document.body.removeChild(overlay);
        document.body.removeChild(dialog);
        callback(true);
    });
    
    document.getElementById('deny-btn').addEventListener('click', () => {
        document.body.removeChild(overlay);
        document.body.removeChild(dialog);
        callback(false);
    });
    
    // Close on overlay click
    overlay.addEventListener('click', () => {
        document.body.removeChild(overlay);
        document.body.removeChild(dialog);
        callback(false);
    });
}

// Test Agent Mode (for debugging)
function testAgentMode() {
    console.log('🤖 Testing Agent Mode...');
    
    const testCommands = [
        { host: 'vm150', command: 'df -h', classification: 'safe', executed: true, result: 'Filesystem      Size  Used Avail Use%\n/dev/vda1       200G   85G  115G  43%' },
        { host: 'vm150', command: 'systemctl restart apache2', classification: 'moderate', executed: false, reason: 'Requires approval' },
        { host: 'vm150', command: 'rm -rf /', classification: 'dangerous', executed: false, reason: 'Blocked - dangerous command' }
    ];
    
    displayAgentExecutions(testCommands);
}

// Export for console testing
window.testAgentMode = testAgentMode;
window.agentModeState = () => ({ enabled: agentModeEnabled, log: agentExecutionLog });
window.fetchSystemMetrics = fetchSystemMetrics;

console.log('🤖 Agent Mode v4.1 loaded - Type testAgentMode() to test');

// (Agent Mode 2FA toggle is handled in initializeAgentMode function above)
// Duplicate handler removed to prevent 2FA conflicts

/*
// DISABLED - This duplicate handler was causing 2FA issues
document.getElementById('agent-mode-checkbox')?.addEventListener('change', async (e) => {
    const checkbox = e.target;
    const statusEl = document.getElementById('agent-mode-status');
    
    if (checkbox.checked) {
        // Prompt for 2FA code
        const code = prompt('🔐 Enter your Google Authenticator code (6 digits):');
        
        if (!code || code.length !== 6 || !/^\d{6}$/.test(code)) {
            checkbox.checked = false;
            alert('❌ Invalid code format. Must be 6 digits.');
            return;
        }
        
        // Show verifying status
        if (statusEl) {
            statusEl.textContent = 'Verifying...';
            statusEl.style.color = '#f39c12';
        }
        
        try {
            const response = await fetch('/verify_2fa.php', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({code: code})
            });
            
            const data = await response.json();
            
            if (data.verified) {
                // Enable Agent Mode
                agentModeVerified = true;
                agentModeEnabled = true;
                
                if (statusEl) {
                    statusEl.textContent = 'Enabled ✓';
                    statusEl.style.color = '#00ff00';
                }
                
                console.log('✅ Agent Mode enabled with 2FA');
                console.log(`⏳ Session expires in ${data.expires_in / 60} minutes`);
                
                // Auto-disable after 1 hour
                agentModeTimeout = setTimeout(() => {
                    checkbox.checked = false;
                    agentModeVerified = false;
                    agentModeEnabled = false;
                    if (statusEl) {
                        statusEl.textContent = 'Disabled';
                        statusEl.style.color = '#aaa';
                    }
                    alert('⏱️ Agent Mode session expired. Re-authenticate to continue.');
                }, data.expires_in * 1000);
                
            } else {
                // Verification failed
                checkbox.checked = false;
                agentModeVerified = false;
                agentModeEnabled = false;
                
                if (statusEl) {
                    statusEl.textContent = 'Disabled';
                    statusEl.style.color = '#aaa';
                }
                
                const attemptsText = data.attempts_remaining !== undefined 
                    ? ` (${data.attempts_remaining} attempts remaining)` 
                    : '';
                alert(`❌ ${data.error || 'Invalid 2FA code'}${attemptsText}`);
            }
        } catch (error) {
            console.error('2FA verification error:', error);
            checkbox.checked = false;
            agentModeVerified = false;
            agentModeEnabled = false;
            
            if (statusEl) {
                statusEl.textContent = 'Disabled';
                statusEl.style.color = '#aaa';
            }
            
            alert('❌ 2FA verification failed. Check console for details.');
        }
    } else {
        // Disable Agent Mode
        agentModeVerified = false;
        agentModeEnabled = false;
        
        if (agentModeTimeout) {
            clearTimeout(agentModeTimeout);
            agentModeTimeout = null;
        }
        
        if (statusEl) {
            statusEl.textContent = 'Disabled';
            statusEl.style.color = '#aaa';
        }
        
        console.log('⚠️ Agent Mode disabled');
    }
});
*/

// API Status Checker
function checkApiStatus() {
    const statusEl = document.getElementById('api-status');
    if (!statusEl) return;
    
    // Add 5-second timeout to detect offline faster
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);
    
    fetch('/api.php', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({action: 'lm_health'}),
        signal: controller.signal
    })
    .then(res => {
        clearTimeout(timeoutId);
        
        // Check if response is OK (status 200-299)
        if (!res.ok) {
            throw new Error(`HTTP ${res.status}`);
        }
        
        return res.json();
    })
    .then(data => {
        if (!data || data.success !== true) {
            const message = (data && data.message) ? data.message : 'LM Studio offline';
            throw new Error(message);
        }

        statusEl.classList.add('online');
        statusEl.classList.remove('offline');
        const textEl = statusEl.querySelector('.status-text');
        if (textEl) {
            const count = typeof data.model_count === 'number' ? data.model_count : 0;
            textEl.textContent = count > 0 ? `LM Studio (${count})` : 'LM Studio Online';
        }
        statusEl.title = data.message || 'LM Studio is online';
        console.log('✅ LM Studio Status: Online');
    })
    .catch((error) => {
        clearTimeout(timeoutId);
        statusEl.classList.add('offline');
        statusEl.classList.remove('online');
        const textEl = statusEl.querySelector('.status-text');
        if (textEl) textEl.textContent = 'LM Studio Offline';
        statusEl.title = error.message || 'LM Studio is not responding';
        console.error('❌ LM Studio Status: Offline -', error.message);
    });
}

// Check API status every 10 seconds (more responsive)
setInterval(checkApiStatus, 10000);
checkApiStatus(); // Initial check

// Python heartbeat checker
function checkPythonHeartbeat() {
    const statusEl = document.getElementById('python-status');
    if (!statusEl) return;

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);

    fetch(API_BASE, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'python_heartbeat' }),
        signal: controller.signal
    })
    .then(res => {
        clearTimeout(timeoutId);
        if (!res.ok) {
            throw new Error(`HTTP ${res.status}`);
        }
        return res.json();
    })
    .then(data => {
        if (!data || data.success !== true) {
            const message = (data && data.message) ? data.message : 'Heartbeat failed';
            throw new Error(message);
        }

        statusEl.classList.add('online');
        statusEl.classList.remove('offline');
        const textEl = statusEl.querySelector('.status-text');
        if (textEl) {
            const latency = typeof data.latency_ms === 'number' ? `${data.latency_ms}ms` : 'Online';
            textEl.textContent = `Heartbeat ${latency}`;
        }
        statusEl.title = data.message || 'Python backend heartbeat OK';
        lastPythonHeartbeat = Date.now();
    })
    .catch(error => {
        clearTimeout(timeoutId);
        statusEl.classList.add('offline');
        statusEl.classList.remove('online');
        const textEl = statusEl.querySelector('.status-text');
        if (textEl) {
            textEl.textContent = 'Heartbeat Offline';
        }
        statusEl.title = error.message || 'Python backend heartbeat failed';
        console.error('❌ Python heartbeat offline -', error.message);
    });
}

setInterval(checkPythonHeartbeat, 15000);
checkPythonHeartbeat();

// ============================================================================
// FAST MODE - Direct LM Studio API Calls (Bypass SHENRON)
// ============================================================================

async function callWarriorDirectly(warriorId, query) {
    const response = await fetch('/api.php', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            fast_mode: true,
            warrior_id: warriorId,
            query: query,
            temperature: 0.7,
            max_tokens: 2000
        })
    });
    
    if (!response.ok) {
        throw new Error(`Warrior ${warriorId} failed: ${response.status}`);
    }
    
    const data = await response.json();
    return data.choices[0].message.content;
}

async function fastModeQuery(query) {
    const warriors = [
        { id: 'Goku-deepseek-coder-v2-lite-instruct', name: 'GOKU', emoji: '🥋' },
        { id: 'Vegeta-llama-3.2-3b-instruct', name: 'VEGETA', emoji: '👑' },
        { id: 'Piccolo-qwen2.5-coder-7b-instruct', name: 'PICCOLO', emoji: '🧘' },
        { id: 'Gohan-mistral-7b-instruct-v0.3', name: 'GOHAN', emoji: '⚠️' },
        { id: 'Krillin-phi-3-mini-128k-instruct', name: 'KRILLIN', emoji: '🔧' },
        { id: 'Frieza-phi-3-mini-128k-instruct', name: 'FRIEZA', emoji: '👹' }
    ];
    
    console.log('⚡ FAST MODE: Querying warriors directly via LM Studio API...');
    
    // Query all warriors in parallel
    const promises = warriors.map(async (warrior) => {
        updateFastModeStatus(warrior.name.toLowerCase(), 'Consulting');
        
        try {
            const response = await callWarriorDirectly(warrior.id, query);
            updateFastModeStatus(warrior.name.toLowerCase(), 'Complete');
            return {
                warrior: warrior.name,
                emoji: warrior.emoji,
                response: response,
                success: true
            };
        } catch (error) {
            console.error(`${warrior.name} failed:`, error);
            updateFastModeStatus(warrior.name.toLowerCase(), 'Failed');
            return {
                warrior: warrior.name,
                emoji: warrior.emoji,
                response: `Error: ${error.message}`,
                success: false
            };
        }
    });
    
    const results = await Promise.all(promises);
    return results;
}

function updateFastModeStatus(warriorName, status) {
    const member = document.querySelector(`[data-member="${warriorName}"]`);
    if (member) {
        const statusDiv = member.querySelector('.member-status');
        if (statusDiv) {
            statusDiv.textContent = status;
            statusDiv.className = 'member-status';
            
            if (status === 'Complete') {
                statusDiv.classList.add('complete');
                triggerRadarPing();
                playSound('warrior-complete');
            } else if (status === 'Failed') {
                statusDiv.classList.add('failed');
                playSound('error');
            } else {
                statusDiv.classList.add('consulting');
            }
        }
    }
    const stateMap = {
        Consulting: { state: 'thinking', text: 'Consulting...' },
        Complete: { state: 'done', text: '✓ Complete' },
        Failed: { state: 'error', text: '✗ Failed' }
    };
    const mapped = stateMap[status] || { state: 'idle', text: 'Ready' };
    updateWarriorStatus(warriorName, mapped.state, mapped.text);
}

function displayFastModeResults(results) {
    const responsesDiv = document.getElementById('warriors-responses');
    if (!responsesDiv) return;
    
    let html = '<div class="fast-mode-results" style="margin-top: 20px;">';
    html += '<h3 style="color: #f39c12; text-align: center; margin-bottom: 20px;">⚡ FAST MODE - Individual Warrior Responses</h3>';
    
    results.forEach(result => {
        const borderColor = result.success ? '#27ae60' : '#e74c3c';
        html += `
            <div class="warrior-response" style="margin-bottom: 20px; padding: 20px; background: rgba(26, 26, 46, 0.8); border-left: 4px solid ${borderColor}; border-radius: 8px;">
                <h4 style="color: #f39c12; margin-bottom: 10px;">
                    ${result.emoji} ${result.warrior}
                </h4>
                <div style="color: #ecf0f1; line-height: 1.6; white-space: pre-wrap;">
                    ${result.response}
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    responsesDiv.innerHTML = html;
    setRadarActive(false);
    setScreenAura(null);
    hideShenronOverlay();
    refreshDragonBallStrip();
}
