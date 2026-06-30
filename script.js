document.addEventListener('DOMContentLoaded', () => {
    // Mobile menu toggle
    const toggle = document.getElementById('mobile-toggle');
    const nav = document.getElementById('nav-links');
    if (toggle && nav) {
        toggle.addEventListener('click', () => {
            nav.classList.toggle('active');
        });
    }

    // Dynamic DSE Snapshot Data Injection
    const snapshotContainer = document.getElementById('dse-snapshot-data');
    if (snapshotContainer) {
        // Illustrative data object
        const marketData = {
            date: "29 June 2026",
            dsei: { value: "2,184.6", change: "+0.4%", positive: true },
            tsi: { value: "4,920.1", change: "+0.3%", positive: true },
            topGainer: { ticker: "NMB", change: "+2.1%", positive: true },
            topLoser: { ticker: "TCC", change: "-1.8%", positive: false }
        };

        const dateEl = document.getElementById('snapshot-date');
        if(dateEl) dateEl.textContent = `As of ${marketData.date}`;

        snapshotContainer.innerHTML = `
            <div class="snapshot-item">
                <div class="snapshot-label">DSEI</div>
                <div class="snapshot-val">${marketData.dsei.value} <span class="${marketData.dsei.positive ? 'text-success' : 'text-danger'}">(${marketData.dsei.change})</span></div>
            </div>
            <div class="snapshot-item">
                <div class="snapshot-label">TSI</div>
                <div class="snapshot-val">${marketData.tsi.value} <span class="${marketData.tsi.positive ? 'text-success' : 'text-danger'}">(${marketData.tsi.change})</span></div>
            </div>
            <div class="snapshot-item">
                <div class="snapshot-label">Top Gainer</div>
                <div class="snapshot-val">${marketData.topGainer.ticker} <span class="text-success">${marketData.topGainer.change}</span></div>
            </div>
            <div class="snapshot-item">
                <div class="snapshot-label">Top Loser</div>
                <div class="snapshot-val">${marketData.topLoser.ticker} <span class="text-danger">${marketData.topLoser.change}</span></div>
            </div>
        `;
    }
});
