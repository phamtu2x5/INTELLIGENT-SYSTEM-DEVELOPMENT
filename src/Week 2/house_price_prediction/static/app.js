/**
 * Minimalist Client JS — House Price Estimator & Real Estate Knowledge Graph
 */

document.addEventListener('DOMContentLoaded', async () => {
    const predictionForm = document.getElementById('predictionForm');
    const submitBtn = document.getElementById('submitBtn');
    const modelSelect = document.getElementById('modelSelect');
    const presetButtons = document.querySelectorAll('.chip-btn');
    
    const singleResultCard = document.getElementById('singleResultCard');
    const comparisonCard = document.getElementById('comparisonCard');
    const mainPrice = document.getElementById('mainPrice');
    const priceM2 = document.getElementById('priceM2');
    const resultBadge = document.getElementById('resultBadge');
    
    const valArea = document.getElementById('valArea');
    const valStructure = document.getElementById('valStructure');
    const valRoads = document.getElementById('valRoads');
    const valSegment = document.getElementById('valSegment');
    
    const avgPrice = document.getElementById('avgPrice');
    const rangePrice = document.getElementById('rangePrice');
    const modelBarsContainer = document.getElementById('modelBarsContainer');

    // Real Estate KG Elements
    const tabFinanceBtn = document.getElementById('tabFinanceBtn');
    const tabGraphBtn = document.getElementById('tabGraphBtn');
    const tabFinanceContent = document.getElementById('tabFinanceContent');
    const tabGraphContent = document.getElementById('tabGraphContent');
    const amenitiesList = document.getElementById('amenitiesList');
    const bankList = document.getElementById('bankList');
    const graphCanvas = document.getElementById('knowledgeGraphCanvas');

    let presetsData = {};
    let currentGraphData = null;

    // 1. Fetch Presets & Models
    try {
        const [presetsRes, modelsRes] = await Promise.all([
            fetch('/api/presets'),
            fetch('/api/models')
        ]);
        const pData = await presetsRes.json();
        pData.presets.forEach(p => {
            presetsData[p.id] = p.data;
        });
    } catch (err) {
        console.error('Error fetching presets/models:', err);
    }

    // 2. Preset Click
    presetButtons.forEach((btn, index) => {
        btn.addEventListener('click', () => {
            presetButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const presetId = btn.dataset.presetId;
            const data = presetsData[presetId];
            if (data) {
                fillFormData(data);
                handlePrediction();
            }
        });

        if (index === 0) {
            btn.classList.add('active');
        }
    });

    function fillFormData(data) {
        if (data.City) document.getElementById('cityInput').value = data.City;
        if (data.District) document.getElementById('districtInput').value = data.District;
        if (data.Ward) document.getElementById('wardInput').value = data.Ward;
        if (data.Area !== undefined) document.getElementById('areaInput').value = data.Area;
        if (data.Frontage !== undefined) document.getElementById('frontageInput').value = data.Frontage;
        if (data['Access Road'] !== undefined) document.getElementById('accessRoadInput').value = data['Access Road'];
        if (data.Floors !== undefined) document.getElementById('floorsInput').value = data.Floors;
        if (data.Bedrooms !== undefined) document.getElementById('bedroomsInput').value = data.Bedrooms;
        if (data.Bathrooms !== undefined) document.getElementById('bathroomsInput').value = data.Bathrooms;
        if (data['Legal status']) document.getElementById('legalSelect').value = data['Legal status'];
        if (data['Furniture state']) document.getElementById('furnitureSelect').value = data['Furniture state'];
    }

    // 3. Model Switch
    modelSelect.addEventListener('change', () => {
        handlePrediction();
    });

    // 4. Form Submit
    predictionForm.addEventListener('submit', (e) => {
        e.preventDefault();
        handlePrediction();
    });

    // 5. Tabs Control
    tabFinanceBtn.addEventListener('click', () => {
        tabFinanceBtn.classList.add('active');
        tabGraphBtn.classList.remove('active');
        tabFinanceContent.style.display = 'block';
        tabGraphContent.style.display = 'none';
    });

    tabGraphBtn.addEventListener('click', () => {
        tabGraphBtn.classList.add('active');
        tabFinanceBtn.classList.remove('active');
        tabFinanceContent.style.display = 'none';
        tabGraphContent.style.display = 'block';
        if (currentGraphData) {
            renderKnowledgeGraph(currentGraphData);
        }
    });

    function getFormPayload() {
        return {
            Area: parseFloat(document.getElementById('areaInput').value) || 50,
            Frontage: parseFloat(document.getElementById('frontageInput').value) || 0,
            'Access Road': parseFloat(document.getElementById('accessRoadInput').value) || 0,
            Floors: parseFloat(document.getElementById('floorsInput').value) || 1,
            Bedrooms: parseFloat(document.getElementById('bedroomsInput').value) || 1,
            Bathrooms: parseFloat(document.getElementById('bathroomsInput').value) || 1,
            'Legal status': document.getElementById('legalSelect').value,
            'Furniture state': document.getElementById('furnitureSelect').value,
            City: document.getElementById('cityInput').value.trim() || 'Unknown',
            District: document.getElementById('districtInput').value.trim() || 'Unknown',
            Ward: document.getElementById('wardInput').value.trim() || 'Unknown',
            model_name: modelSelect.value
        };
    }

    // 6. Predict Handler
    async function handlePrediction() {
        const payload = getFormPayload();
        const isAllModels = payload.model_name === 'ALL';

        submitBtn.classList.add('loading');
        submitBtn.querySelector('.btn-text').innerText = 'Đang tính toán...';

        try {
            if (isAllModels) {
                const res = await fetch('/api/predict-all', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (data.status === 'success') {
                    renderAllModelsResult(data);
                }
            } else {
                const res = await fetch('/api/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (data.status === 'success') {
                    renderSingleModelResult(data);
                    if (data.amenities) {
                        renderAmenities(data.amenities);
                    }
                    if (data.financial_package) {
                        renderBankLoans(data.financial_package);
                    }
                    if (data.knowledge_graph) {
                        currentGraphData = data.knowledge_graph;
                        if (tabGraphContent.style.display !== 'none') {
                            renderKnowledgeGraph(currentGraphData);
                        }
                    }
                }
            }
        } catch (err) {
            console.error('Prediction error:', err);
        } finally {
            submitBtn.classList.remove('loading');
            submitBtn.querySelector('.btn-text').innerText = 'Định giá & Phân tích Tri thức';
        }
    }

    // 7. Render Single Result
    function renderSingleModelResult(data) {
        singleResultCard.style.display = 'block';
        comparisonCard.style.display = 'none';

        resultBadge.innerText = data.display_name;
        mainPrice.innerText = data.price_formatted;
        priceM2.innerText = data.price_per_m2_formatted;

        const areaVal = parseFloat(areaInput.value) || 85;
        const floorsVal = parseInt(floorsInput.value) || 3;
        const bedroomsVal = parseInt(bedroomsInput.value) || 4;
        const frontageVal = parseFloat(frontageInput.value) || 4.5;
        const accessRoadVal = parseFloat(accessRoadInput.value) || 6.0;

        const valAreaEl = document.getElementById('valArea');
        const valStructureEl = document.getElementById('valStructure');
        const valRoadsEl = document.getElementById('valRoads');
        const valSegmentEl = document.getElementById('valSegment');

        if (valAreaEl) valAreaEl.innerText = `${areaVal} m²`;
        if (valStructureEl) valStructureEl.innerText = `${floorsVal} Tầng • ${bedroomsVal} PN`;
        if (valRoadsEl) valRoadsEl.innerText = `${frontageVal}m / ${accessRoadVal}m`;

        if (valSegmentEl) {
            let segment = "Nhà phố Đô thị";
            if (areaVal >= 200 || (data.price_billion && data.price_billion >= 15)) {
                segment = "Biệt thự Cao cấp";
            } else if (areaVal < 45) {
                segment = "Nhà ngõ diện tích nhỏ";
            }
            valSegmentEl.innerText = segment;
        }
    }

    // 8. Render All Models Comparison
    function renderAllModelsResult(data) {
        singleResultCard.style.display = 'none';
        comparisonCard.style.display = 'block';

        avgPrice.innerText = `TB: ${data.summary.average_formatted}`;
        rangePrice.innerText = `Khoảng giá: ${data.summary.price_range}`;

        const results = data.results;
        const maxPrice = Math.max(...results.map(r => r.price_billion));

        modelBarsContainer.innerHTML = '';
        results.forEach(item => {
            const percentage = maxPrice > 0 ? (item.price_billion / maxPrice) * 100 : 50;
            const barRow = document.createElement('div');
            barRow.className = `model-bar-item ${item.is_best ? 'best' : ''}`;
            barRow.innerHTML = `
                <div class="bar-row-top">
                    <span>${item.is_best ? '🏆 ' : ''}${item.display_name}</span>
                    <span>${item.price_formatted}</span>
                </div>
                <div class="bar-row-track">
                    <div class="bar-row-fill" style="width: ${percentage.toFixed(1)}%;"></div>
                </div>
                <div class="bar-row-bottom">
                    <span>Đơn giá: ${item.price_per_m2_formatted}</span>
                    <span>${item.badge || item.type}</span>
                </div>
            `;
            modelBarsContainer.appendChild(barRow);
        });
    }

    // 9. Render Amenities
    function renderAmenities(amenities) {
        amenitiesList.innerHTML = '';
        if (amenities && amenities.length > 0) {
            amenities.forEach(am => {
                const card = document.createElement('div');
                card.className = 'amenity-card';
                card.innerHTML = `
                    <div class="am-left">
                        <span class="am-icon">${am.icon || '📍'}</span>
                        <div>
                            <div class="am-name">${am.name}</div>
                            <div class="am-type">${am.type}</div>
                        </div>
                    </div>
                    <span class="am-dist">${am.distance}</span>
                `;
                amenitiesList.appendChild(card);
            });
        }
    }

    // 10. Render Bank Mortgage Loans
    function renderBankLoans(finPackage) {
        bankList.innerHTML = '';
        if (finPackage && finPackage.banks) {
            finPackage.banks.forEach(b => {
                const m = b.mortgage;
                const card = document.createElement('div');
                card.className = 'bank-card';
                card.innerHTML = `
                    <div class="b-top">
                        <span class="b-name">${b.bank_name}</span>
                        <span class="b-rate">Lãi: ${b.preferential_rate_pct}%/năm</span>
                    </div>
                    <div class="b-details">
                        <span>Hạn mức: ${m.loan_amount_formatted} (${b.max_ltv_pct}%)</span>
                        <span class="b-monthly">Góp: ${m.monthly_estimate_formatted}</span>
                    </div>
                    <div class="b-highlight">${b.highlight}</div>
                `;
                bankList.appendChild(card);
            });
        }
    }

    // 11. Knowledge Graph 2D Canvas Renderer
    function renderKnowledgeGraph(graphData) {
        if (!graphCanvas) return;
        const ctx = graphCanvas.getContext('2d');
        const width = graphCanvas.width = graphCanvas.parentElement.clientWidth || 960;
        const height = graphCanvas.height = 380;

        ctx.clearRect(0, 0, width, height);

        const nodes = graphData.nodes || [];
        const edges = graphData.edges || [];

        const centerX = width / 2;
        const centerY = height / 2;
        const positions = {};

        // Assign fixed pleasant radial positions
        nodes.forEach((n, i) => {
            if (n.id === 'property') {
                positions[n.id] = { x: centerX - 120, y: centerY };
            } else if (n.id === 'location') {
                positions[n.id] = { x: centerX - 260, y: centerY - 60 };
            } else if (n.id === 'valuation') {
                positions[n.id] = { x: centerX + 110, y: centerY - 60 };
            } else if (n.id === 'bank_loan') {
                positions[n.id] = { x: centerX + 270, y: centerY - 60 };
            } else if (n.id === 'broker') {
                positions[n.id] = { x: centerX + 110, y: centerY + 100 };
            } else if (n.group === 'amenity') {
                positions[n.id] = { x: centerX - 260, y: centerY + 40 + (i % 3) * 55 };
            } else {
                const angle = (i / nodes.length) * 2 * Math.PI;
                positions[n.id] = {
                    x: centerX + Math.cos(angle) * 180,
                    y: centerY + Math.sin(angle) * 120
                };
            }
        });

        // 1. Draw Edges
        edges.forEach(e => {
            const p1 = positions[e.from];
            const p2 = positions[e.to];
            if (p1 && p2) {
                ctx.beginPath();
                ctx.moveTo(p1.x, p1.y);
                ctx.lineTo(p2.x, p2.y);
                ctx.strokeStyle = e.color || '#475569';
                ctx.lineWidth = 1.5;
                ctx.stroke();

                // Edge label
                const midX = (p1.x + p2.x) / 2;
                const midY = (p1.y + p2.y) / 2;
                ctx.font = '9px Inter, sans-serif';
                ctx.fillStyle = '#94a3b8';
                ctx.textAlign = 'center';
                ctx.fillText(e.label || '', midX, midY - 3);
            }
        });

        // 2. Draw Nodes
        nodes.forEach(n => {
            const pos = positions[n.id];
            if (pos) {
                const r = n.size ? n.size / 2 : 12;

                // Glow ring
                ctx.beginPath();
                ctx.arc(pos.x, pos.y, r + 4, 0, 2 * Math.PI);
                ctx.fillStyle = (n.color || '#2563eb') + '22';
                ctx.fill();

                // Circle body
                ctx.beginPath();
                ctx.arc(pos.x, pos.y, r, 0, 2 * Math.PI);
                ctx.fillStyle = n.color || '#2563eb';
                ctx.fill();
                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 2;
                ctx.stroke();

                // Text Label
                ctx.font = '10px Inter, sans-serif';
                ctx.fillStyle = '#f8fafc';
                ctx.textAlign = 'center';
                ctx.fillText(n.label || n.id, pos.x, pos.y + r + 13);
            }
        });
    }

    // Initial Trigger
    setTimeout(() => {
        handlePrediction();
    }, 150);
});
