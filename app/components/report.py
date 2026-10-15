"""Generador de Informes de Auditoría Personalizados para descarga (HTML y CSV)."""

from datetime import datetime

from src.schemas import ActuarialImpactResult, ActuarialProfile


def generate_audit_report_html(
    profile: ActuarialProfile,
    impact: ActuarialImpactResult,
    afp_real_return_pct: float,
    afp_swaps_damage_pp: float,
) -> str:
    """Genera un informe ejecutivo en HTML formateado para visualización e impresión a PDF."""
    fecha_emision = datetime.now().strftime("%d-%m-%Y %H:%M")
    
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Informe de Auditoría Forense — Fondo E</title>
    <style>
        body {{
            font-family: 'Helvetica Neue', Arial, sans-serif;
            background-color: #0D1117;
            color: #F8FAFC;
            margin: 0;
            padding: 40px;
            line-height: 1.5;
        }}
        .header {{
            border-bottom: 2px solid #D90429;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .title {{
            font-size: 26px;
            font-weight: 800;
            color: #F8FAFC;
            margin: 0 0 6px 0;
        }}
        .subtitle {{
            font-size: 14px;
            color: #8B949E;
            margin: 0;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .meta-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            background: #161B22;
            border: 1px solid #30363D;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 30px;
        }}
        .meta-item strong {{
            color: #8B949E;
            display: block;
            font-size: 11px;
            text-transform: uppercase;
        }}
        .meta-item span {{
            font-size: 16px;
            font-weight: 600;
            color: #F8FAFC;
        }}
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 30px;
        }}
        .kpi-box {{
            background: #1A2230;
            border: 1px solid #30363D;
            border-radius: 8px;
            padding: 16px;
            text-align: center;
        }}
        .kpi-box .label {{
            font-size: 11px;
            color: #8B949E;
            text-transform: uppercase;
            margin-bottom: 6px;
        }}
        .kpi-box .val {{
            font-size: 20px;
            font-weight: 800;
            color: #FF4D6D;
        }}
        .section-title {{
            font-size: 18px;
            font-weight: 700;
            color: #F8FAFC;
            margin: 25px 0 12px 0;
            border-left: 4px solid #D90429;
            padding-left: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 25px;
            font-size: 13px;
        }}
        th, td {{
            padding: 10px 14px;
            text-align: left;
            border-bottom: 1px solid #30363D;
        }}
        th {{
            background-color: #161B22;
            color: #8B949E;
            text-transform: uppercase;
            font-size: 11px;
        }}
        tr:nth-child(even) {{
            background-color: #11151C;
        }}
        .callout {{
            background: #161B22;
            border: 1px solid #D90429;
            border-radius: 8px;
            padding: 16px;
            font-size: 12px;
            color: #C9D1D9;
            margin-bottom: 30px;
        }}
        .footer {{
            border-top: 1px solid #30363D;
            padding-top: 15px;
            font-size: 11px;
            color: #6E7681;
            text-align: center;
        }}
        @media print {{
            body {{
                background-color: #FFFFFF !important;
                color: #000000 !important;
                padding: 20px;
            }}
            .meta-grid, .kpi-box, th, tr:nth-child(even), .callout {{
                background-color: #F8FAFC !important;
                color: #000000 !important;
                border-color: #CBD5E1 !important;
            }}
            .title, .subtitle, .meta-item span, .section-title {{
                color: #000000 !important;
            }}
            .kpi-box .val {{
                color: #DC2626 !important;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1 class="title">INFORME FORENSE DE IMPACTO ACTUARIAL — FONDO E</h1>
        <p class="subtitle">Auditoría del Colapso 2026 y Cuantificación de Daño Previsional</p>
    </div>

    <div class="meta-grid">
        <div class="meta-item">
            <strong>Afiliado / Administradora</strong>
            <span>AFP {profile.afp}</span>
        </div>
        <div class="meta-item">
            <strong>Fecha de Emisión</strong>
            <span>{fecha_emision}</span>
        </div>
        <div class="meta-item">
            <strong>Perfil Demográfico</strong>
            <span>{profile.sexo.capitalize()}, {profile.edad_actual} años (Retiro a los {profile.edad_jubilacion} años)</span>
        </div>
        <div class="meta-item">
            <strong>Tasa Técnica Aplicada</strong>
            <span>{profile.tasa_tecnica * 100:.2f}% Real Anual (Tablas RV-2020)</span>
        </div>
    </div>

    <div class="kpi-grid">
        <div class="kpi-box">
            <div class="label">Pérdida Total 2026</div>
            <div class="val">-${impact.perdida_patrimonial_clp:,.0f} CLP</div>
        </div>
        <div class="kpi-box">
            <div class="label">Daño por Swaps</div>
            <div class="val">-${impact.perdida_swaps_clp:,.0f} CLP</div>
        </div>
        <div class="kpi-box">
            <div class="label">Recorte Pensión Mensual</div>
            <div class="val">-${impact.recorte_pension_mensual:,.0f} CLP/mes</div>
        </div>
        <div class="kpi-box">
            <div class="label">Meses Trabajo Extra (P50)</div>
            <div class="val">{impact.monte_carlo_meses_recuperacion_p50:.0f} meses</div>
        </div>
    </div>

    <div class="section-title">1. Resumen Patrimonial y Actuarial</div>
    <table>
        <thead>
            <tr>
                <th>Concepto</th>
                <th>Valor Pre-Shock</th>
                <th>Valor Post-Shock</th>
                <th>Variación / Recorte</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Saldo Acumulado en Fondo E</strong></td>
                <td>${impact.saldo_inicial_estimado:,.0f} CLP</td>
                <td>${impact.saldo_post_shock:,.0f} CLP</td>
                <td><span style="color:#FF4D6D;">-${impact.perdida_patrimonial_clp:,.0f} CLP ({afp_real_return_pct:.2f}%)</span></td>
            </tr>
            <tr>
                <td><strong>Pérdida por Derivados y Swaps (80%)</strong></td>
                <td>$0 CLP</td>
                <td>-${impact.perdida_swaps_clp:,.0f} CLP</td>
                <td><span style="color:#FF4D6D;">{afp_swaps_damage_pp:.2f} puntos porcentuales</span></td>
            </tr>
            <tr>
                <td><strong>Capital Necesario Unitario (CNU)</strong></td>
                <td>{impact.cnu:.4f} años</td>
                <td>{impact.cnu:.4f} años</td>
                <td>Factor actuarial fijo RV-2020</td>
            </tr>
            <tr>
                <td><strong>Pensión Mensual Vitalicia Autofinanciada</strong></td>
                <td>${impact.pension_pre_shock_mensual:,.0f} CLP/mes</td>
                <td>${impact.pension_post_shock_mensual:,.0f} CLP/mes</td>
                <td><span style="color:#FF4D6D;">-${impact.recorte_pension_mensual:,.0f} CLP/mes (-{impact.recorte_pension_pct:.2f}%)</span></td>
            </tr>
        </tbody>
    </table>

    <div class="section-title">2. Estimación de Recuperación (Simulación de Monte Carlo)</div>
    <table>
        <thead>
            <tr>
                <th>Escenario Estocástico</th>
                <th>Horizonte Estimado</th>
                <th>Interpretación</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>P10 (Escenario Favorable)</strong></td>
                <td>{impact.monte_carlo_meses_recuperacion_p10:.0f} meses</td>
                <td>Recuperación rápida bajo rebaja acelerada de tasas y fuerte aporte previsional.</td>
            </tr>
            <tr>
                <td><strong>P50 (Mediana Esperada)</strong></td>
                <td>{impact.monte_carlo_meses_recuperacion_p50:.0f} meses ({impact.monte_carlo_meses_recuperacion_p50 / 12:.1f} años)</td>
                <td>Tiempo esperado de postergación del retiro para reponer el capital perdido.</td>
            </tr>
            <tr>
                <td><strong>P90 (Escenario Severo)</strong></td>
                <td>{impact.monte_carlo_meses_recuperacion_p90:.0f} meses</td>
                <td>Persistencia de tasas elevadas en EE.UU. o volatilidad prolongada.</td>
            </tr>
        </tbody>
    </table>

    <div class="callout">
        <strong>Nota Metodológica y Legal:</strong> La pensión calculada corresponde a la modalidad de pensión autofinanciada (Retiro Programado / Renta Vitalicia contributiva pura) calculada conforme al D.L. 3.500 con las tablas de mortalidad oficiales RV-2020 y la tasa técnica de descuento seleccionada. No incluye suplementos del Estado como la Pensión Garantizada Universal (PGU).
    </div>

    <div class="footer">
        Documento generado automáticamente por la Plataforma de Auditoría Forense del Fondo E.<br>
        Microdatos certificados de la Superintendencia de Pensiones, Banco Central de Chile y Reserva Federal.
    </div>
</body>
</html>
"""
    return html


def generate_audit_csv(
    profile: ActuarialProfile,
    impact: ActuarialImpactResult,
    afp_real_return_pct: float,
    afp_swaps_damage_pp: float,
) -> str:
    """Genera un archivo CSV estructurado con todas las métricas del cálculo."""
    lines = [
        "variable,valor,unidad,descripcion",
        f"afp,{profile.afp},texto,Administradora de Fondos de Pensiones",
        f"edad_actual,{profile.edad_actual},anios,Edad actual del afiliado",
        f"sexo,{profile.sexo},texto,Sexo para tablas de mortalidad RV-2020",
        f"edad_jubilacion,{profile.edad_jubilacion},anios,Edad proyectada de retiro",
        f"sueldo_imponible,{profile.sueldo_imponible:.0f},CLP,Sueldo imponible mensual",
        f"tasa_tecnica,{profile.tasa_tecnica:.4f},tasa,Tasa tecnica anual de descuento",
        f"saldo_inicial_estimado,{impact.saldo_inicial_estimado:.0f},CLP,Saldo previo al colapso de 2026",
        f"saldo_post_shock,{impact.saldo_post_shock:.0f},CLP,Saldo actual tras el colapso",
        f"retorno_real_afp_pct,{afp_real_return_pct:.2f},%,Retorno real acumulado 2026",
        f"perdida_patrimonial_clp,{impact.perdida_patrimonial_clp:.0f},CLP,Perdida patrimonial neta",
        f"danio_swaps_pp,{afp_swaps_damage_pp:.2f},pp,Puntos porcentuales de perdida por swaps",
        f"perdida_swaps_clp,{impact.perdida_swaps_clp:.0f},CLP,Perdida en pesos atribuible a swaps",
        f"cnu_rv2020,{impact.cnu:.4f},factor,Capital Necesario Unitario Woolhouse",
        f"pension_pre_shock_mensual,{impact.pension_pre_shock_mensual:.0f},CLP/mes,Pension mensual vitalicia estimada pre-shock",
        f"pension_post_shock_mensual,{impact.pension_post_shock_mensual:.0f},CLP/mes,Pension mensual vitalicia post-shock",
        f"recorte_pension_mensual,{impact.recorte_pension_mensual:.0f},CLP/mes,Recorte permanente en la pension mensual",
        f"recorte_pension_pct,{impact.recorte_pension_pct:.2f},%,Porcentaje de recorte permanente",
        f"monte_carlo_meses_p10,{impact.monte_carlo_meses_recuperacion_p10:.1f},meses,Escenario favorable de recuperacion",
        f"monte_carlo_meses_p50,{impact.monte_carlo_meses_recuperacion_p50:.1f},meses,Mediana de meses de trabajo extra requeridos",
        f"monte_carlo_meses_p90,{impact.monte_carlo_meses_recuperacion_p90:.1f},meses,Escenario severo de recuperacion",
    ]
    return "\n".join(lines)
