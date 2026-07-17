// Amana Capital East Africa - Main Application Script

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize SPA Router (Swup)
    const swup = new Swup({
        animationSelector: '[class*="transition-"]',
        cache: true
    });

    // 2. Initialize modules on first load
    initMobileMenu();
    initBondCalculator();

    // 3. Re-initialize modules after every page transition
    swup.hooks.on('page:view', () => {
        initMobileMenu();
        initBondCalculator();
        
        // Re-initialize Weglot if present
        if (typeof Weglot !== 'undefined') {
            Weglot.initialize({ api_key: 'wg_22a6f434974df4dee513e25f34fc5e009' });
        }
        
        // Scroll to top on transition
        window.scrollTo(0, 0);
    });
});

// --- Mobile Navigation Logic ---
window.initMobileMenu = function() {
    const toggle = document.getElementById('mobile-toggle');
    const nav = document.getElementById('nav-links');
    
    if (toggle && nav) {
        // Remove old listeners by cloning (prevents duplicates since navbar persists)
        const newToggle = toggle.cloneNode(true);
        toggle.parentNode.replaceChild(newToggle, toggle);
        
        newToggle.addEventListener('click', () => {
            nav.classList.toggle('active');
        });
    }
};

// --- Bond Calculator Logic ---
window.initBondCalculator = function() {
    const fvInput = document.getElementById('fv');
    if (!fvInput) return; // Exit if we are not on the bond calculator page

    let progChart = null;
    
    // Inputs
    const crInput = document.getElementById('cr');
    const myInput = document.getElementById('my');
    const ppyInput = document.getElementById('ppy');
    const mpInput = document.getElementById('mp');
    const dslcInput = document.getElementById('dslc');
    
    // Call Options
    const isCallCheckbox = document.getElementById('isCall');
    const callInputsDiv = document.getElementById('call-inputs');
    const cyInput = document.getElementById('cy');
    const cpInput = document.getElementById('cp');

    // Outputs
    const outAi = document.getElementById('out-ai');
    const outDp = document.getElementById('out-dp');
    const outYtm = document.getElementById('out-ytm');
    const outYtc = document.getElementById('out-ytc');
    const outYtw = document.getElementById('out-ytw');
    const stressMatrix = document.getElementById('stress-matrix');
    
    const invAmtInput = document.getElementById('invAmt');
    const inflInput = document.getElementById('infl');
    const outRealYield = document.getElementById('out-real-yield');
    const progressionTable = document.getElementById('progression-table');
    
    const outStartCap = document.getElementById('out-start-cap');
    const outTotalCash = document.getElementById('out-total-cash');
    const outTotalProfit = document.getElementById('out-total-profit');

    // Toggle Call Inputs
    isCallCheckbox.addEventListener('change', () => {
        callInputsDiv.style.display = isCallCheckbox.checked ? 'block' : 'none';
        calculateAnalytics();
    });

    // Attach listeners
    const inputs = [fvInput, crInput, myInput, ppyInput, mpInput, dslcInput, cyInput, cpInput, invAmtInput, inflInput];
    inputs.forEach(input => {
        input.addEventListener('input', calculateAnalytics);
    });

    function solveYield(targetPrice, periods, redemptionValue, fv, cr, ppy, dslc, dicp = 180) {
        let lowY = 0.0;
        let highY = 2.0; 
        const tolerance = 1e-6;
        let y = 0.0;
        const couponPayment = (fv * cr) / ppy;
        
        for (let i = 0; i < 100; ++i) {
            y = (lowY + highY) / 2.0;
            const periodYield = y / ppy;
            let price = 0.0;
            const w = 1.0 - (dslc / dicp);
            for (let t = 0; t < periods; ++t) {
                price += couponPayment / Math.pow(1 + periodYield, w + t);
            }
            price += redemptionValue / Math.pow(1 + periodYield, w + (periods - 1));
            
            if (Math.abs(price - targetPrice) < tolerance) { return y; }
            if (price > targetPrice) { lowY = y; } else { highY = y; }
        }
        return y;
    }

    function calculateRiskMetrics(targetYield, targetPeriods, targetRedemption, fv, cr, ppy, dslc, dirtyPrice) {
        const periodYield = targetYield / ppy;
        const couponPayment = (fv * cr) / ppy;
        const dicp = 180;
        const w = 1.0 - (dslc / dicp);
        
        let macDuration = 0.0;
        let convexity = 0.0;
        let calculatedPrice = 0.0;
        
        for (let t = 0; t < targetPeriods; ++t) {
            const timeInPeriods = w + t;
            const timeInYears = timeInPeriods / ppy;
            const presentValue = couponPayment / Math.pow(1 + periodYield, timeInPeriods);
            
            calculatedPrice += presentValue;
            macDuration += (timeInYears * presentValue);
            convexity += (timeInYears * (timeInYears + (1.0 / ppy)) * presentValue);
        }
        
        const redemptionPV = targetRedemption / Math.pow(1 + periodYield, w + (targetPeriods - 1));
        calculatedPrice += redemptionPV;
        const redemptionTime = w + (targetPeriods - 1);
        macDuration += ((redemptionTime / ppy) * redemptionPV);
        convexity += ((redemptionTime / ppy) * ((redemptionTime / ppy) + (1.0 / ppy)) * redemptionPV);
        
        macDuration = macDuration / calculatedPrice;
        const modDuration = macDuration / (1 + periodYield);
        convexity = convexity / calculatedPrice;
        
        return { modDuration, convexity };
    }

    function generateStressMatrix(baseYield, targetPeriods, targetRedemption, fv, cr, ppy, dslc) {
        const shocks = [-0.02, -0.01, -0.005, 0.005, 0.01, 0.02];
        let html = '';
        const couponPayment = (fv * cr) / ppy;
        const dicp = 180;
        const w = 1.0 - (dslc / dicp);
        
        shocks.forEach((s, i) => {
            const shockedYield = baseYield + s;
            const shockedPeriodYield = shockedYield / ppy;
            let p = 0.0;
            
            for (let t = 0; t < targetPeriods; ++t) {
                p += couponPayment / Math.pow(1 + shockedPeriodYield, w + t);
            }
            p += targetRedemption / Math.pow(1 + shockedPeriodYield, w + (targetPeriods - 1));
            
            const pctPriceStr = ((p / fv) * 100).toFixed(4);
            const bps = s * 10000;
            const sign = bps > 0 ? '+' : '';
            const color = bps > 0 ? 'var(--loss)' : 'var(--gain)';
            
            const rowBg = i % 2 !== 0 ? 'background: rgba(255,255,255,0.02);' : '';
            html += `<tr style="${rowBg}">
                <td style="padding: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.05);">${sign}${bps} bps</td>
                <td style="padding: 0.5rem; text-align:right; border-bottom: 1px solid rgba(255,255,255,0.05); color:${color}; font-weight:600;">${sign}${(s * 100).toFixed(1)}%</td>
                <td style="padding: 0.5rem; text-align:right; border-bottom: 1px solid rgba(255,255,255,0.05);">${pctPriceStr}</td>
            </tr>`;
        });
        return html;
    }

    function renderProgressionChart(labels, principalData, incomeData) {
        const canvas = document.getElementById('progressionChart');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        
        if (progChart) progChart.destroy();
        
        if (typeof Chart === 'undefined') return;

        progChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Total Accumulated Value',
                        data: principalData,
                        borderColor: '#C8962E',
                        backgroundColor: 'rgba(200, 150, 46, 0.1)',
                        fill: true,
                        tension: 0.3,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Cumulative Income Drawn',
                        data: incomeData,
                        borderColor: '#16A34A',
                        borderDash: [5, 5],
                        fill: false,
                        tension: 0.3,
                        yAxisID: 'y'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: { mode: 'index', intersect: false },
                plugins: {
                    legend: { labels: { color: '#E8E2D9' } }
                },
                scales: {
                    x: { ticks: { color: '#9A9490' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                    y: { ticks: { color: '#9A9490' }, grid: { color: 'rgba(255,255,255,0.05)' } }
                }
            }
        });
    }

    function formatCurrency(val) {
        return val.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
    }

    function calculateAnalytics() {
        const fv = parseFloat(fvInput.value) || 0;
        const cr = parseFloat(crInput.value) / 100.0;
        const my = parseFloat(myInput.value) || 0;
        const ppy = parseInt(ppyInput.value) || 2;
        const mp = parseFloat(mpInput.value) || 0;
        const dslc = parseInt(dslcInput.value) || 0;
        const isCall = isCallCheckbox.checked;
        const cy = parseFloat(cyInput.value) || 0;
        const cp = parseFloat(cpInput.value) || 100.0;
        
        const invAmt = parseFloat(invAmtInput.value) || 0;
        const infl = parseFloat(inflInput.value) / 100.0;

        if (fv <= 0 || my <= 0 || ppy <= 0 || mp <= 0) {
            return;
        }

        const dicp = 180; 
        const periodCoupon = (fv * cr) / ppy;
        const ai = periodCoupon * (dslc / dicp);
        const aiPct = (ai / fv) * 100;
        const cleanPrice = mp;
        const dirtyPrice = cleanPrice + aiPct;
        const priceValue = (dirtyPrice / 100) * fv;

        outAi.textContent = `${aiPct.toFixed(4)}`;
        outDp.textContent = `${dirtyPrice.toFixed(4)}`;

        const matPeriods = Math.ceil(my * ppy);
        const matRedemption = fv;
        const ytm = solveYield(priceValue, matPeriods, matRedemption, fv, cr, ppy, dslc);
        outYtm.textContent = (ytm * 100).toFixed(4) + '%';

        let activeYield = ytm;
        let activePeriods = matPeriods;
        let activeRedemption = matRedemption;

        if (isCall && cy > 0) {
            const callPeriods = Math.ceil(cy * ppy);
            const callRedemption = fv * (cp / 100.0);
            const ytc = solveYield(priceValue, callPeriods, callRedemption, fv, cr, ppy, dslc);
            outYtc.textContent = (ytc * 100).toFixed(4) + '%';
            
            if (ytc < ytm) {
                outYtw.textContent = (ytc * 100).toFixed(4) + '% (YTC)';
                activeYield = ytc;
                activePeriods = callPeriods;
                activeRedemption = callRedemption;
            } else {
                outYtw.textContent = (ytm * 100).toFixed(4) + '% (YTM)';
            }
        } else {
            outYtc.textContent = "N/A";
            outYtw.textContent = (ytm * 100).toFixed(4) + '% (YTM)';
        }

        stressMatrix.innerHTML = generateStressMatrix(activeYield, activePeriods, activeRedemption, fv, cr, ppy, dslc);
        const realYield = activeYield - infl;
        outRealYield.textContent = (realYield * 100).toFixed(2) + '%';

        if (invAmt > 0) {
            const bondsPurchased = invAmt / (dirtyPrice / 100.0 * 100); 
            const annualIncome = bondsPurchased * 100 * cr;
            let totalCashReturned = 0;
            let totalProfit = 0;
            let currentRealValue = invAmt;
            let cumIncome = 0;

            const maxYears = isCall && cy > 0 && cy < my ? cy : my;
            let tableHtml = '';
            
            const labels = [];
            const principalData = [];
            const incomeData = [];

            labels.push('Year 0');
            principalData.push(invAmt);
            incomeData.push(0);

            for (let year = 1; year <= Math.ceil(maxYears); year++) {
                let thisYearIncome = annualIncome;
                let isMaturityYear = false;
                
                if (year > maxYears) {
                    const frac = 1 - (year - maxYears);
                    thisYearIncome = annualIncome * frac;
                    isMaturityYear = true;
                } else if (year === Math.ceil(maxYears)) {
                    isMaturityYear = true;
                }

                cumIncome += thisYearIncome;
                totalCashReturned += thisYearIncome;
                
                let nominalValue = invAmt + cumIncome;
                currentRealValue = (invAmt) / Math.pow(1 + infl, year) + cumIncome;
                
                if (isMaturityYear) {
                    const redemp = bondsPurchased * 100 * (isCall && cy > 0 && cy < my ? cp/100.0 : 1.0);
                    totalCashReturned += redemp;
                    nominalValue += redemp - invAmt; 
                }

                labels.push(`Year ${year}`);
                principalData.push(nominalValue);
                incomeData.push(cumIncome);

                const rowBg = year % 2 === 0 ? 'background: rgba(255,255,255,0.02);' : '';
                tableHtml += `<tr style="${rowBg}">
                    <td style="padding: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.05);">${year}${isMaturityYear ? ' (Mat/Call)' : ''}</td>
                    <td style="padding: 0.5rem; text-align:right; border-bottom: 1px solid rgba(255,255,255,0.05);">TZS ${formatCurrency(thisYearIncome)}</td>
                    <td style="padding: 0.5rem; text-align:right; border-bottom: 1px solid rgba(255,255,255,0.05);">TZS ${formatCurrency(cumIncome)}</td>
                    <td style="padding: 0.5rem; text-align:right; border-bottom: 1px solid rgba(255,255,255,0.05); font-weight:600;">TZS ${formatCurrency(currentRealValue)}</td>
                </tr>`;
            }

            totalProfit = totalCashReturned - invAmt;
            outStartCap.textContent = `TZS ${formatCurrency(invAmt)}`;
            outTotalCash.textContent = `TZS ${formatCurrency(totalCashReturned)}`;
            outTotalProfit.textContent = `TZS ${formatCurrency(totalProfit)}`;
            progressionTable.innerHTML = tableHtml;

            renderProgressionChart(labels, principalData, incomeData);
        } else {
            outStartCap.textContent = "0";
            outTotalCash.textContent = "0";
            outTotalProfit.textContent = "0";
            progressionTable.innerHTML = "";
            if (progChart) {
                progChart.destroy();
                progChart = null;
            }
        }
    }

    // Trigger initial calculation
    calculateAnalytics();
};
