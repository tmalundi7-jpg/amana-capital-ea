document.addEventListener('DOMContentLoaded', () => {
    // Inputs
    const fvInput = document.getElementById('fv');
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
    
    // Phase 6 Additions
    const invAmtInput = document.getElementById('invAmt');
    const inflInput = document.getElementById('infl');
    const outRealYield = document.getElementById('out-real-yield');
    const progressionTable = document.getElementById('progression-table');

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

    // --- Financial Logic (Ported from C++) ---

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
            
            if (Math.abs(price - targetPrice) < tolerance) {
                return y;
            }
            if (price > targetPrice) {
                lowY = y;
            } else {
                highY = y;
            }
        }
        return y;
    }

    function calculateRiskMetrics(targetYield, targetPeriods, targetRedemption, fv, cr, ppy, dslc, dirtyPrice) {
        const periodYield = targetYield / ppy;
        const couponPayment = (fv * cr) / ppy;
        const dicp = 180; // assume 180 days in semi-annual period for simple math
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
        const maturityTimeInYears = (w + (targetPeriods - 1)) / ppy;
        
        calculatedPrice += redemptionPV;
        macDuration += (maturityTimeInYears * redemptionPV);
        convexity += (maturityTimeInYears * (maturityTimeInYears + (1.0 / ppy)) * redemptionPV);
        
        macDuration /= calculatedPrice;
        const modDuration = macDuration / (1 + periodYield);
        convexity /= (calculatedPrice * Math.pow(1 + periodYield, 2));

        return { modDuration, convexity };
    }

    function calculateAnalytics() {
        // Read values
        const fv = parseFloat(fvInput.value) || 0;
        const cr = (parseFloat(crInput.value) || 0) / 100.0;
        const my = parseInt(myInput.value) || 0;
        const ppy = parseInt(ppyInput.value) || 2;
        const mp = parseFloat(mpInput.value) || 0;
        const dslc = parseInt(dslcInput.value) || 0;
        
        const isCall = isCallCheckbox.checked;
        const cy = parseInt(cyInput.value) || 0;
        const cp = parseFloat(cpInput.value) || 0;

        const invAmt = parseFloat(invAmtInput.value) || 0;
        const infl = (parseFloat(inflInput.value) || 0) / 100.0;

        // Base Calculations
        const dicp = 180;
        const couponPayment = (fv * cr) / ppy;
        const accruedInterest = couponPayment * (dslc / dicp);
        const dirtyPrice = mp + accruedInterest;

        // Outputs updates
        outAi.innerText = accruedInterest.toFixed(4);
        outDp.innerText = dirtyPrice.toFixed(4);

        if (fv === 0 || my === 0 || mp === 0) return;

        // Yield to Maturity
        const ytm = solveYield(dirtyPrice, my * ppy, fv, fv, cr, ppy, dslc, dicp);
        outYtm.innerText = (ytm * 100).toFixed(4) + '%';

        let ytw = ytm;
        let activePeriods = my * ppy;
        let activeRedemption = fv;

        // Yield to Call
        if (isCall && cy > 0) {
            const ytc = solveYield(dirtyPrice, cy * ppy, cp, fv, cr, ppy, dslc, dicp);
            outYtc.innerText = (ytc * 100).toFixed(4) + '%';
            if (ytc < ytm) {
                ytw = ytc;
                activePeriods = cy * ppy;
                activeRedemption = cp;
            }
        } else {
            outYtc.innerText = 'N/A';
        }

        outYtw.innerText = (ytw * 100).toFixed(4) + '%';

        // Real Yield
        const realYield = ((1 + ytw) / (1 + infl)) - 1;
        outRealYield.innerText = (realYield * 100).toFixed(4) + '%';
        outRealYield.style.color = realYield < 0 ? 'var(--loss)' : 'var(--gold)';

        // Stress Matrix
        const metrics = calculateRiskMetrics(ytw, activePeriods, activeRedemption, fv, cr, ppy, dslc, dirtyPrice);
        const modDur = metrics.modDuration;
        const conv = metrics.convexity;

        const shocks = [-0.02, -0.01, -0.005, 0.005, 0.01, 0.02];
        const shockLabels = ["-200 bps", "-100 bps", "-50 bps", "+50 bps", "+100 bps", "+200 bps"];
        
        stressMatrix.innerHTML = '';
        
        for (let i = 0; i < shocks.length; i++) {
            const s = shocks[i];
            const pctChange = (-modDur * s) + (0.5 * conv * s * s);
            const newPrice = mp * (1 + pctChange);
            
            const tr = document.createElement('tr');
            if (i % 2 !== 0) tr.style.background = 'rgba(255,255,255,0.02)';
            
            const tdShock = document.createElement('td');
            tdShock.innerText = shockLabels[i];
            
            const tdImpact = document.createElement('td');
            tdImpact.style.textAlign = 'right';
            tdImpact.style.fontWeight = '600';
            tdImpact.style.color = pctChange > 0 ? 'var(--gain)' : 'var(--loss)';
            tdImpact.innerText = (pctChange > 0 ? '+' : '') + (pctChange * 100).toFixed(2) + '%';

            const tdPrice = document.createElement('td');
            tdPrice.style.textAlign = 'right';
            tdPrice.innerText = newPrice.toFixed(4);

            tr.appendChild(tdShock);
            tr.appendChild(tdImpact);
            tr.appendChild(tdPrice);
            stressMatrix.appendChild(tr);
        }

        // Progression Table
        progressionTable.innerHTML = '';
        if (invAmt > 0 && my > 0 && dirtyPrice > 0) {
            // Assume quoted price is per 100 of Face Value. Number of bonds = Investment / dirtyPrice.
            // Face Value Owned = (Investment / dirtyPrice) * 100
            // But since 'fv' is customizable, we do (Investment / dirtyPrice) * fv
            const fvOwned = (invAmt / dirtyPrice) * fv;
            
            const yearlyCouponIncome = fvOwned * cr;
            let cumNominal = 0;
            let cumReal = 0;
            
            for (let year = 1; year <= my; year++) {
                let nominalCashFlow = yearlyCouponIncome;
                
                if (year === my) {
                    nominalCashFlow += fvOwned;
                }
                
                cumNominal += nominalCashFlow;
                
                const realCashFlow = nominalCashFlow / Math.pow(1 + infl, year);
                cumReal += realCashFlow;
                
                const tr = document.createElement('tr');
                if (year % 2 === 0) tr.style.background = 'rgba(255,255,255,0.02)';
                
                const tdYear = document.createElement('td');
                tdYear.innerText = 'Year ' + year;
                
                const tdIncome = document.createElement('td');
                tdIncome.style.textAlign = 'right';
                tdIncome.innerText = nominalCashFlow.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
                
                const tdCumNom = document.createElement('td');
                tdCumNom.style.textAlign = 'right';
                tdCumNom.innerText = cumNominal.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
                
                const tdCumReal = document.createElement('td');
                tdCumReal.style.textAlign = 'right';
                tdCumReal.style.fontWeight = '600';
                tdCumReal.innerText = cumReal.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
                
                tr.appendChild(tdYear);
                tr.appendChild(tdIncome);
                tr.appendChild(tdCumNom);
                tr.appendChild(tdCumReal);
                progressionTable.appendChild(tr);
            }
        }
    }

    // Initial run
    calculateAnalytics();
});
