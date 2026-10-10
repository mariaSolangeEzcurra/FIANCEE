
import { useEffect, useMemo, useState } from 'react'
import { apiRequest } from '../../services/api.js'

const EMPTY_FORM = {
  fecha_entrega_solicitada: '',
  importe_propuesto: '',
  dinero_recibido_proyectado: '',
  productos: [
    {
      nombre: '',
      tipo_producto: '',
      tipo_trabajo: '',
      origen_taller: '',
      fecha_entrega: '',
      horas_estimadas: '',
      observaciones: '',
    },
  ],
}

const PRODUCT_TYPES = [
  'Novia',
  'Quinceañera',
  'Vestido de cambio',
  'Desmontable',
  'Velo',
  'Mini me',
  'Accesorio',
  'Otro',
]

const WORK_TYPES = ['Confección', 'Bordado', 'Entalle', 'Acabados', 'Otro']
const WORKSHOPS = ['Taller A', 'Taller C', 'Otro']

const styles = {
  page: {
    minHeight: '100%',
    padding: '28px',
    background: '#faf8f6',
    color: '#342a2b',
    fontFamily: 'Inter, system-ui, sans-serif',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    gap: 20,
    flexWrap: 'wrap',
    marginBottom: 28,
  },
  eyebrow: {
    margin: '0 0 8px',
    color: '#9a7655',
    fontSize: 12,
    fontWeight: 800,
    letterSpacing: 2,
    textTransform: 'uppercase',
  },
  title: {
    margin: 0,
    fontSize: 'clamp(25px, 3vw, 34px)',
    letterSpacing: -0.8,
  },
  subtitle: {
    margin: '10px 0 0',
    maxWidth: 650,
    color: '#786f70',
    fontSize: 14,
    lineHeight: 1.7,
  },
  button: {
    border: 0,
    borderRadius: 10,
    background: '#765345',
    color: '#fff',
    padding: '12px 18px',
    fontWeight: 700,
    cursor: 'pointer',
  },
  secondaryButton: {
    border: '1px solid #e5d9d2',
    borderRadius: 9,
    background: '#fff',
    color: '#765345',
    padding: '10px 14px',
    fontWeight: 700,
    cursor: 'pointer',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(190px, 1fr))',
    gap: 15,
    marginBottom: 24,
  },
  card: {
    border: '1px solid #eee5df',
    borderRadius: 15,
    background: '#fff',
    padding: 20,
    minWidth: 0,
  },
  metricLabel: {
    margin: 0,
    color: '#817677',
    fontSize: 13,
  },
  metricValue: {
    margin: '13px 0 7px',
    fontSize: 29,
    fontWeight: 800,
    letterSpacing: -0.7,
  },
  muted: {
    color: '#938889',
    fontSize: 12,
    lineHeight: 1.6,
  },
  sectionTitle: {
    margin: '0 0 5px',
    fontSize: 18,
  },
  sectionDescription: {
    margin: '0 0 20px',
    color: '#827677',
    fontSize: 13,
    lineHeight: 1.6,
  },
  formGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(210px, 1fr))',
    gap: 16,
  },
  field: {
    display: 'flex',
    flexDirection: 'column',
    gap: 7,
    minWidth: 0,
  },
  label: {
    fontSize: 12,
    fontWeight: 700,
    color: '#65595a',
  },
  input: {
    width: '100%',
    minWidth: 0,
    boxSizing: 'border-box',
    border: '1px solid #e6dcd6',
    borderRadius: 9,
    padding: '11px 12px',
    background: '#fff',
    color: '#342a2b',
    font: 'inherit',
    fontSize: 13,
  },
  divider: {
    height: 1,
    border: 0,
    background: '#f0e8e3',
    margin: '22px 0',
  },
  productCard: {
    padding: 17,
    border: '1px solid #eee5df',
    borderRadius: 12,
    marginBottom: 14,
    background: '#fdfcfb',
  },
  notice: {
    border: '1px solid #e9d9c7',
    background: '#fcf6ee',
    color: '#755b43',
    borderRadius: 11,
    padding: 14,
    fontSize: 13,
    lineHeight: 1.7,
    marginBottom: 20,
  },
  resultBox: {
    borderRadius: 12,
    padding: 18,
    background: '#f8f4f1',
    border: '1px solid #eee3dc',
  },
  footerActions: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: 10,
    marginTop: 22,
  },
}

function MetricCard({ label, value, description }) {
  return (
    <article style={styles.card}>
      <p style={styles.metricLabel}>{label}</p>
      <p style={styles.metricValue}>{value}</p>
      <span style={styles.muted}>{description}</span>
    </article>
  )
}

function Field({ label, children }) {
  return (
    <label style={styles.field}>
      <span style={styles.label}>{label}</span>
      {children}
    </label>
  )
}

function Input({ value, onChange, type = 'text', min, step, placeholder }) {
  return (
    <input
      style={styles.input}
      type={type}
      value={value}
      onChange={onChange}
      min={min}
      step={step}
      placeholder={placeholder}
    />
  )
}

function Select({ value, onChange, options, placeholder }) {
  return (
    <select
      style={styles.input}
      value={value}
      onChange={onChange}
    >
      <option value="">{placeholder || 'Seleccionar'}</option>
      {options.map((option) => (
        <option key={option} value={option}>
          {option}
        </option>
      ))}
    </select>
  )
}

function formatNumber(value, decimals = 1) {
  if (value === null || value === undefined || value === '') return '—'

  const number = Number(value)
  if (!Number.isFinite(number)) return '—'

  return new Intl.NumberFormat('es-PE', {
    maximumFractionDigits: decimals,
  }).format(number)
}

function getErrorMessage(error) {
  return error instanceof Error
    ? error.message
    : 'Ocurrió un error al consultar el servidor.'
}

export default function Simulator() {
  const [summary, setSummary] = useState(null)
  const [summaryLoading, setSummaryLoading] = useState(true)
  const [summaryError, setSummaryError] = useState('')
  const [form, setForm] = useState(EMPTY_FORM)
  const [saving, setSaving] = useState(false)
  const [saveMessage, setSaveMessage] = useState('')
  const [saveError, setSaveError] = useState('')

  const [sessionToken, setSessionToken] = useState(() => {
    try {
      const stored = localStorage.getItem('token')
      return stored || ''
    } catch {
      return ''
    }
  })

  useEffect(() => {
    let active = true

    async function loadSummary() {
      setSummaryLoading(true)
      setSummaryError('')

      try {
        // El endpoint pertenece al backend de capacidad revisado.
        const result = await apiRequest('/capacidad/resumen/', {
          token: sessionToken || undefined,
        })

        if (active) setSummary(result)
      } catch (error) {
        if (active) {
          setSummary(null)
          setSummaryError(getErrorMessage(error))
        }
      } finally {
        if (active) setSummaryLoading(false)
      }
    }

    loadSummary()

    return () => {
      active = false
    }
  }, [sessionToken])

  const metrics = useMemo(() => {
    if (!summary) {
      return [
        {
          label: 'Personal activo',
          value: '—',
          description: 'No se pudo obtener el resumen.',
        },
        {
          label: 'Horas pendientes',
          value: '—',
          description: 'No se pudo obtener el resumen.',
        },
        {
          label: 'Operaciones pendientes',
          value: '—',
          description: 'No se pudo obtener el resumen.',
        },
        {
          label: 'Simulaciones registradas',
          value: '—',
          description: 'No se pudo obtener el resumen.',
        },
      ]
    }

    return [
      {
        label: 'Personal activo',
        value: formatNumber(summary.trabajadoras_activas, 0),
        description: 'Trabajadoras activas registradas.',
      },
      {
        label: 'Horas pendientes',
        value: formatNumber(
          summary.horas_estimadas_pendientes_o_en_curso,
        ),
        description: 'Horas estimadas de operaciones abiertas.',
      },
      {
        label: 'Operaciones pendientes',
        value: formatNumber(
          summary.operaciones_pendientes_o_en_curso,
          0,
        ),
        description: 'Operaciones pendientes o en curso.',
      },
      {
        label: 'Simulaciones registradas',
        value: formatNumber(summary.simulaciones, 0),
        description: 'Simulaciones guardadas en el sistema.',
      },
    ]
  }, [summary])

  function updateForm(field, value) {
    setForm((current) => ({ ...current, [field]: value }))
    setSaveMessage('')
    setSaveError('')
  }

  function updateProduct(index, field, value) {
    setForm((current) => ({
      ...current,
      productos: current.productos.map((product, productIndex) =>
        productIndex === index
          ? { ...product, [field]: value }
          : product,
      ),
    }))
    setSaveMessage('')
    setSaveError('')
  }

  function addProduct() {
    setForm((current) => ({
      ...current,
      productos: [
        ...current.productos,
        { ...EMPTY_FORM.productos[0] },
      ],
    }))
  }

  function removeProduct(index) {
    setForm((current) => ({
      ...current,
      productos: current.productos.filter(
        (_, productIndex) => productIndex !== index,
      ),
    }))
  }

  const totalHours = useMemo(
    () =>
      form.productos.reduce(
        (total, product) => total + (Number(product.horas_estimadas) || 0),
        0,
      ),
    [form.productos],
  )

  const canSubmit =
    Boolean(form.fecha_entrega_solicitada) &&
    form.productos.length > 0 &&
    form.productos.every(
      (product) =>
        product.nombre.trim() &&
        product.tipo_producto &&
        product.tipo_trabajo &&
        product.origen_taller &&
        product.fecha_entrega &&
        product.horas_estimadas !== '' &&
        Number(product.horas_estimadas) >= 0,
    ) &&
    form.importe_propuesto !== '' &&
    Number(form.importe_propuesto) >= 0 &&
    form.dinero_recibido_proyectado !== '' &&
    Number(form.dinero_recibido_proyectado) >= 0

  async function handleSubmit(event) {
    event.preventDefault()
    setSaveMessage('')
    setSaveError('')

    if (!canSubmit) {
      setSaveError(
        'Completa los campos obligatorios y revisa las horas y los importes.',
      )
      return
    }

    setSaving(true)

    try {
      // Este endpoint crea el registro de simulación.
      // Los productos se registran por separado para respetar los modelos actuales.
      const simulation = await apiRequest('/capacidad/simulaciones/', {
        method: 'POST',
        token: sessionToken || undefined,
        body: JSON.stringify({
          fecha_entrega_solicitada: form.fecha_entrega_solicitada,
          importe_propuesto: Number(form.importe_propuesto),
          dinero_recibido_proyectado: Number(
            form.dinero_recibido_proyectado,
          ),
          horas_requeridas: totalHours,
          resultado: 'pendiente',
          resumen_resultado:
            'Simulación registrada. La factibilidad requiere evaluar la capacidad real.',
        }),
      })

      for (const product of form.productos) {
        await apiRequest('/capacidad/productos-simulacion/', {
          method: 'POST',
          token: sessionToken || undefined,
          body: JSON.stringify({
            ...product,
            simulacion: simulation.id,
            horas_estimadas: Number(product.horas_estimadas),
          }),
        })
      }

      setSaveMessage(
        `Simulación ${simulation.id} registrada. El resultado queda pendiente de evaluación de capacidad.`,
      )
      setForm(EMPTY_FORM)

      const refreshedSummary = await apiRequest('/capacidad/resumen/', {
        token: sessionToken || undefined,
      })
      setSummary(refreshedSummary)
    } catch (error) {
      setSaveError(getErrorMessage(error))
    } finally {
      setSaving(false)
    }
  }

  return (
    <main style={styles.page}>
      <header style={styles.header}>

      </header>


      <form onSubmit={handleSubmit}>
        <section style={{ ...styles.card, marginBottom: 22 }}>
          <h2 style={styles.sectionTitle}>01 · Datos de la simulación</h2>
          <p style={styles.sectionDescription}>
            Registra la fecha solicitada y los importes de la propuesta
            comercial.
          </p>

          <div style={styles.formGrid}>
            <Field label="Fecha de entrega solicitada *">
              <Input
                type="date"
                value={form.fecha_entrega_solicitada}
                onChange={(event) =>
                  updateForm(
                    'fecha_entrega_solicitada',
                    event.target.value,
                  )
                }
              />
            </Field>

            <Field label="Importe propuesto (S/) *">
              <Input
                type="number"
                min="0"
                step="0.01"
                placeholder="Ingresar importe"
                value={form.importe_propuesto}
                onChange={(event) =>
                  updateForm('importe_propuesto', event.target.value)
                }
              />
            </Field>

            <Field label="Dinero recibido proyectado (S/) *">
              <Input
                type="number"
                min="0"
                step="0.01"
                placeholder="Ingresar importe"
                value={form.dinero_recibido_proyectado}
                onChange={(event) =>
                  updateForm(
                    'dinero_recibido_proyectado',
                    event.target.value,
                  )
                }
              />
            </Field>
          </div>
        </section>

        <section style={{ ...styles.card, marginBottom: 22 }}>
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              flexWrap: 'wrap',
              gap: 12,
              marginBottom: 6,
            }}
          >
            <h2 style={styles.sectionTitle}>02 · Vestidos a evaluar</h2>
            <button
              type="button"
              style={styles.secondaryButton}
              onClick={addProduct}
            >
              + Añadir vestido
            </button>
          </div>

          <p style={styles.sectionDescription}>
            Completa las características y las horas previstas de cada
            producto. Las horas introducidas son una estimación para esta
            simulación, no tiempos estándar de la base de datos.
          </p>

          {form.productos.map((product, index) => (
            <div key={index} style={styles.productCard}>
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  gap: 12,
                  marginBottom: 17,
                }}
              >
                <strong style={{ fontSize: 14 }}>
                  Vestido {String(index + 1).padStart(2, '0')}
                </strong>

                {form.productos.length > 1 && (
                  <button
                    type="button"
                    style={{
                      ...styles.secondaryButton,
                      color: '#9d4c4c',
                      padding: '7px 10px',
                    }}
                    onClick={() => removeProduct(index)}
                  >
                    Quitar
                  </button>
                )}
              </div>

              <div style={styles.formGrid}>
                <Field label="Nombre o referencia *">
                  <Input
                    placeholder="Nombre del diseño"
                    value={product.nombre}
                    onChange={(event) =>
                      updateProduct(index, 'nombre', event.target.value)
                    }
                  />
                </Field>

                <Field label="Tipo de producto *">
                  <Select
                    value={product.tipo_producto}
                    options={PRODUCT_TYPES}
                    placeholder="Seleccionar tipo"
                    onChange={(event) =>
                      updateProduct(
                        index,
                        'tipo_producto',
                        event.target.value,
                      )
                    }
                  />
                </Field>

                <Field label="Tipo de trabajo *">
                  <Select
                    value={product.tipo_trabajo}
                    options={WORK_TYPES}
                    placeholder="Seleccionar trabajo"
                    onChange={(event) =>
                      updateProduct(
                        index,
                        'tipo_trabajo',
                        event.target.value,
                      )
                    }
                  />
                </Field>

                <Field label="Taller de origen *">
                  <Select
                    value={product.origen_taller}
                    options={WORKSHOPS}
                    placeholder="Seleccionar taller"
                    onChange={(event) =>
                      updateProduct(
                        index,
                        'origen_taller',
                        event.target.value,
                      )
                    }
                  />
                </Field>

                <Field label="Fecha de entrega del vestido *">
                  <Input
                    type="date"
                    value={product.fecha_entrega}
                    onChange={(event) =>
                      updateProduct(
                        index,
                        'fecha_entrega',
                        event.target.value,
                      )
                    }
                  />
                </Field>

                <Field label="Horas estimadas *">
                  <Input
                    type="number"
                    min="0"
                    step="0.5"
                    placeholder="Horas previstas"
                    value={product.horas_estimadas}
                    onChange={(event) =>
                      updateProduct(
                        index,
                        'horas_estimadas',
                        event.target.value,
                      )
                    }
                  />
                </Field>

                <div style={{ ...styles.field, gridColumn: '1 / -1' }}>
                  <span style={styles.label}>Observaciones</span>
                  <textarea
                    style={{
                      ...styles.input,
                      minHeight: 75,
                      resize: 'vertical',
                    }}
                    value={product.observaciones}
                    placeholder="Detalles adicionales del vestido"
                    onChange={(event) =>
                      updateProduct(
                        index,
                        'observaciones',
                        event.target.value,
                      )
                    }
                  />
                </div>
              </div>
            </div>
          ))}

          <div style={styles.resultBox}>
            <p style={{ ...styles.metricLabel, marginBottom: 8 }}>
              Total de horas estimadas ingresadas
            </p>
            <strong style={{ fontSize: 25 }}>
              {formatNumber(totalHours)} h
            </strong>
            <p style={{ ...styles.muted, marginBottom: 0 }}>
              Esta suma no representa disponibilidad real ni confirma
              que el taller pueda asumir el trabajo.
            </p>
          </div>
        </section>

        <section style={styles.card}>
          <h2 style={styles.sectionTitle}>03 · Resultado</h2>
          <p style={styles.sectionDescription}>
            La simulación se registra con estado pendiente. Todavía no se
            determina automáticamente si la fecha solicitada es viable.
          </p>

          <div style={styles.resultBox}>
            <p style={styles.metricLabel}>Estado de factibilidad</p>
            <h3 style={{ margin: '10px 0', fontSize: 21 }}>
              Pendiente de evaluación
            </h3>
            <p style={{ ...styles.muted, marginBottom: 0 }}>
              Para evaluar la capacidad necesitamos los horarios,
              las habilidades, los centros de trabajo, las operaciones
              y sus dependencias.
            </p>
          </div>

          {saveError && (
            <div role="alert" style={{ ...styles.notice, marginTop: 18 }}>
              <strong>No se pudo registrar la simulación.</strong>
              <div>{saveError}</div>
            </div>
          )}

          {saveMessage && (
            <div
              role="status"
              style={{
                ...styles.notice,
                marginTop: 18,
                borderColor: '#c9dfcf',
                background: '#f0f8f1',
                color: '#356344',
              }}
            >
              {saveMessage}
            </div>
          )}

          <div style={styles.footerActions}>
            <button
              type="submit"
              style={{
                ...styles.button,
                opacity: saving || !canSubmit ? 0.65 : 1,
                cursor: saving || !canSubmit ? 'not-allowed' : 'pointer',
              }}
              disabled={saving || !canSubmit}
            >
              {saving ? 'Registrando…' : 'Registrar simulación'}
            </button>

            <button
              type="button"
              style={styles.secondaryButton}
              disabled={saving}
              onClick={() => {
                setForm(EMPTY_FORM)
                setSaveMessage('')
                setSaveError('')
              }}
            >
              Limpiar formulario
            </button>
          </div>

          <p style={{ ...styles.muted, marginTop: 15, marginBottom: 0 }}>
            El registro guarda la simulación y sus productos. Si ocurre
            un error durante el guardado, revisa la lista de simulaciones
            antes de volver a enviarla para evitar duplicados.
          </p>
        </section>
      </form>
    </main>
  )
}
