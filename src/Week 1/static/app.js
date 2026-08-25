/**
 * Minimalist Client JS — Diabetes Diagnostic & FPT Long Châu Knowledge Graph
 */

document.addEventListener('DOMContentLoaded', async () => {
    const predictionForm = document.getElementById('predictionForm');
    const submitBtn = document.getElementById('submitBtn');
    const modelSelect = document.getElementById('modelSelect');
    const presetButtons = document.querySelectorAll('.chip-btn');
    
    const singleResultCard = document.getElementById('singleResultCard');
    const comparisonCard = document.getElementById('comparisonCard');
    const resultBadge = document.getElementById('resultBadge');
    
    const statusBanner = document.getElementById('statusBanner');
    const statusHeadline = document.getElementById('statusHeadline');
    const riskProbValue = document.getElementById('riskProbValue');
    const probFill = document.getElementById('probFill');
    const adviceText = document.getElementById('adviceText');
    
    const valRocAuc = document.getElementById('valRocAuc');
    const valAcc = document.getElementById('valAcc');
    const valF1 = document.getElementById('valF1');
    const valRecall = document.getElementById('valRecall');
    
    const avgProb = document.getElementById('avgProb');
    const consensusText = document.getElementById('consensusText');
    const modelBarsContainer = document.getElementById('modelBarsContainer');

    // Long Chau & Knowledge Graph Elements
    const tabProductsBtn = document.getElementById('tabProductsBtn');
    const tabGraphBtn = document.getElementById('tabGraphBtn');
    const tabProductsContent = document.getElementById('tabProductsContent');
    const tabGraphContent = document.getElementById('tabGraphContent');
    const devicesList = document.getElementById('devicesList');
    const supplementsList = document.getElementById('supplementsList');
    const nearestStoreText = document.getElementById('nearestStoreText');
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
        if (pData.presets.length > 0) {
            fillFormData(pData.presets[0].data);
            handlePrediction();
        }
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
        if (data.Pregnancies !== undefined) document.getElementById('pregInput').value = data.Pregnancies;
        if (data.Glucose !== undefined) document.getElementById('glucoseInput').value = data.Glucose;
        if (data.BloodPressure !== undefined) document.getElementById('bpInput').value = data.BloodPressure;
        if (data.SkinThickness !== undefined) document.getElementById('skinInput').value = data.SkinThickness;
        if (data.Insulin !== undefined) document.getElementById('insulinInput').value = data.Insulin;
        if (data.BMI !== undefined) document.getElementById('bmiInput').value = data.BMI;
        if (data.DiabetesPedigreeFunction !== undefined) document.getElementById('dpfInput').value = data.DiabetesPedigreeFunction;
        if (data.Age !== undefined) document.getElementById('ageInput').value = data.Age;
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
    tabProductsBtn.addEventListener('click', () => {
        tabProductsBtn.classList.add('active');
        tabGraphBtn.classList.remove('active');
        tabProductsContent.style.display = 'block';
        tabGraphContent.style.display = 'none';
    });

    tabGraphBtn.addEventListener('click', () => {
        tabGraphBtn.classList.add('active');
        tabProductsBtn.classList.remove('active');
        tabProductsContent.style.display = 'none';
        tabGraphContent.style.display = 'block';
        if (currentGraphData) {
            renderKnowledgeGraph(currentGraphData);
        }
    });

    function getFormPayload() {
        return {
            Pregnancies: parseFloat(document.getElementById('pregInput').value) || 0,
            Glucose: parseFloat(document.getElementById('glucoseInput').value) || 100,
            BloodPressure: parseFloat(document.getElementById('bpInput').value) || null,
            SkinThickness: parseFloat(document.getElementById('skinInput').value) || null,
            Insulin: parseFloat(document.getElementById('insulinInput').value) || null,
            BMI: parseFloat(document.getElementById('bmiInput').value) || 25.0,
            DiabetesPedigreeFunction: parseFloat(document.getElementById('dpfInput').value) || 0.47,
            Age: parseFloat(document.getElementById('ageInput').value) || 30,
            model_name: modelSelect.value
        };
    }

    // 6. Predict Handler
    async function handlePrediction() {
        const payload = getFormPayload();
        const isAllModels = payload.model_name === 'ALL';

        submitBtn.classList.add('loading');
        submitBtn.querySelector('.btn-text').innerText = 'Đang phân tích...';

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
                    if (data.longchau_care) {
                        renderLongChauCare(data.longchau_care);
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
            submitBtn.querySelector('.btn-text').innerText = 'Chẩn đoán & Phân tích Tri thức';
        }
    }

    // 7. Render Single Result
    function renderSingleModelResult(data) {
        singleResultCard.style.display = 'block';
        comparisonCard.style.display = 'none';

        resultBadge.innerText = data.display_name;
        
        statusBanner.className = `status-banner ${data.status_color}`;
        statusHeadline.innerText = data.status_text;
        riskProbValue.innerText = `Xác suất rủi ro: ${data.diabetic_probability}%`;
        probFill.style.width = `${data.diabetic_probability}%`;
        adviceText.innerText = data.advice;

        const glucoseVal = document.getElementById('glucoseInput').value || 100;
        const bmiVal = document.getElementById('bmiInput').value || 25.0;

        const valIcd = document.getElementById('valIcd');
        const valThreshold = document.getElementById('valThreshold');
        const valGlucoseBio = document.getElementById('valGlucoseBio');
        const valBmiBio = document.getElementById('valBmiBio');

        if (valIcd) valIcd.innerText = data.diabetic_probability >= 25.0 ? 'ICD-10 E11' : 'Bình thường';
        if (valThreshold) valThreshold.innerText = 'θ ≥ 0.25';
        if (valGlucoseBio) valGlucoseBio.innerText = `${glucoseVal} mg/dL`;
        if (valBmiBio) valBmiBio.innerText = `${bmiVal} kg/m²`;
    }

    // 8. Render All Models Comparison
    function renderAllModelsResult(data) {
        singleResultCard.style.display = 'none';
        comparisonCard.style.display = 'block';

        avgProb.innerText = `TB: ${data.summary.average_formatted}`;
        consensusText.innerText = data.summary.consensus;

        const results = data.results;
        modelBarsContainer.innerHTML = '';
        
        results.forEach(item => {
            const prob = item.diabetic_probability;
            const barRow = document.createElement('div');
            barRow.className = `model-bar-item ${item.is_best ? 'best' : ''}`;
            barRow.innerHTML = `
                <div class="bar-row-top">
                    <span>${item.is_best ? '🏆 ' : ''}${item.display_name}</span>
                    <span>${item.prob_formatted}</span>
                </div>
                <div class="bar-row-track">
                    <div class="bar-row-fill" style="width: ${prob}%;"></div>
                </div>
                <div class="bar-row-bottom">
                    <span>${item.prediction === 1 ? '🔴 Dương tính' : '🟢 Âm tính'}</span>
                    <span>ROC-AUC: ${item.roc_auc} | Acc: ${item.accuracy}%</span>
                </div>
            `;
            modelBarsContainer.appendChild(barRow);
        });
    }

    // 9. Render Long Châu Care Products
    function renderLongChauCare(care) {
        // Devices
        devicesList.innerHTML = '';
        if (care.devices && care.devices.length > 0) {
            care.devices.forEach(d => {
                const card = document.createElement('div');
                card.className = 'product-card';
                card.innerHTML = `
                    <div class="p-left">
                        <span class="p-tag">${d.tag}</span>
                        <a href="${d.url}" target="_blank" class="p-name">${d.name}</a>
                        <span class="p-benefit">${d.benefit}</span>
                    </div>
                    <div class="p-right">
                        <div class="p-price">${d.price_formatted}</div>
                        <a href="${d.url}" target="_blank" class="p-buy-btn">Mua tại Long Châu ➔</a>
                    </div>
                `;
                devicesList.appendChild(card);
            });
        } else {
            devicesList.innerHTML = '<p style="font-size:0.8rem; color:#64748b;">Chỉ số tốt, không yêu cầu thiết bị chuyên sâu.</p>';
        }

        // Supplements
        supplementsList.innerHTML = '';
        if (care.supplements && care.supplements.length > 0) {
            care.supplements.forEach(s => {
                const card = document.createElement('div');
                card.className = 'product-card';
                card.innerHTML = `
                    <div class="p-left">
                        <span class="p-tag">${s.tag}</span>
                        <a href="${s.url}" target="_blank" class="p-name">${s.name}</a>
                        <span class="p-benefit">${s.benefit}</span>
                    </div>
                    <div class="p-right">
                        <div class="p-price">${s.price_formatted}</div>
                        <a href="${s.url}" target="_blank" class="p-buy-btn">Mua tại Long Châu ➔</a>
                    </div>
                `;
                supplementsList.appendChild(card);
            });
        }

        // Store
        if (care.store) {
            nearestStoreText.innerText = `${care.store.name} (Hotline: ${care.store.hotline})`;
        }
    }

    // 10. Knowledge Graph 2D Canvas Renderer
    function renderKnowledgeGraph(graphData) {
        if (!graphCanvas) return;
        const ctx = graphCanvas.getContext('2d');
        const width = graphCanvas.width = graphCanvas.parentElement.clientWidth || 960;
        const height = graphCanvas.height = 380;

        ctx.clearRect(0, 0, width, height);

        const nodes = graphData.nodes || [];
        const edges = graphData.edges || [];

        // Simple Radial Layout
        const centerX = width / 2;
        const centerY = height / 2;
        const positions = {};

        // Assign fixed pleasant positions
        nodes.forEach((n, i) => {
            if (n.id === 'patient') {
                positions[n.id] = { x: centerX - 260, y: centerY };
            } else if (n.id === 'prediction') {
                positions[n.id] = { x: centerX - 80, y: centerY - 70 };
            } else if (n.id === 'disease') {
                positions[n.id] = { x: centerX + 90, y: centerY - 60 };
            } else if (n.id === 'bio_glucose') {
                positions[n.id] = { x: centerX - 260, y: centerY - 110 };
            } else if (n.id === 'bio_bmi') {
                positions[n.id] = { x: centerX - 260, y: centerY + 110 };
            } else if (n.id === 'store_01') {
                positions[n.id] = { x: centerX - 60, y: centerY + 110 };
            } else if (n.group === 'device') {
                positions[n.id] = { x: centerX + 270, y: centerY - 90 + (i % 2) * 50 };
            } else if (n.group === 'supplement') {
                positions[n.id] = { x: centerX + 270, y: centerY + 60 + (i % 2) * 50 };
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
    setTimeout(async () => {
        await handlePrediction();
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('tab') === 'graph') {
            tabGraphBtn.click();
        }
    }, 150);
});
