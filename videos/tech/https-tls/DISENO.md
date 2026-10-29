# Diseño: short "How HTTPS works" (TLS), todo en 3D

Estado: Aldo dio luz verde total el 2026-10-28 ("ya todo es luz verde, al igual que el siguiente tema del video HTTPS y TLS"). Se hace sin supervisión después del de DNS, con las mismas reglas y piezas (`videos/tech/dns/DISENO.md`).

## Intención

Segundo short de la línea "cómo funcionan las tecnologías". Explica qué agrega HTTPS a HTTP: privacidad, integridad y saber con quién hablas, con el saludo de TLS contado en una aldea de Minecraft. Todo en 3D, voz madura clonada, música de C418, menos de 3 minutos.

## La metáfora

- Steve es tu navegador. El banco ("mybank.com") es el servidor, con un banquero aldeano.
- El camino entre los dos está lleno de ojos: el vendedor ambulante del video de DNS lee todo lo que pasa abierto.
- **HTTP** = mandar un libro abierto por el camino.
- **Certificado** = una etiqueta de nombre (name tag) que dice "mybank.com", sellada (brillo de encantamiento) por un clérigo: la **autoridad certificadora** (CA). Steve trae un libro con los clérigos en los que confía (la lista de su navegador).
- El banco **demuestra que tiene la llave secreta** de esa etiqueta: un ladrón con una copia de la etiqueta no puede.
- **Intercambio de llaves (Diffie-Hellman)** = mezclar tintes de lana: color público amarillo; Steve agrega rojo en secreto y manda naranja; el banco agrega azul en secreto y manda verde; cada uno agrega su secreto a lo que recibió y los dos llegan al mismo café. El espía ve amarillo, naranja y verde, nunca rojo ni azul.
- **Cifrado simétrico** = cada mensaje viaja en un cofre cerrado con el café. Si alguien lo abre o lo cambia, el sello se rompe y el mensaje se tira (integridad).
- **El candado** del navegador = todo lo anterior salió bien. No dice que el sitio sea honesto: "myb4nk.com" también puede tener candado.

## Narración

En `narration.txt` (nombres y siglas escritos como se dicen). Unas 330 palabras, ~115 s.

## Exactitud

- TLS 1.3: el cliente saluda con su parte de la llave; el servidor contesta con la suya, su certificado y una firma del saludo hecha con la llave privada del certificado. La CA firma el certificado que une el nombre con la llave pública; el navegador trae una lista de CAs raíz en las que confía.
- Diffie-Hellman efímero: los dos llegan al mismo secreto sin mandarlo nunca. La pintura es la analogía clásica: mezclar es fácil, separar no.
- Después del saludo todo va con cifrado simétrico autenticado (AEAD): si un mensaje se altera, no pasa la verificación y se descarta.
- Un sitio de phishing puede tener un certificado válido para su propio nombre: el candado no prueba honestidad.
- No decir que HTTPS esconde qué sitio visitas: el nombre todavía puede verse (DNS, SNI). El guion no lo menciona.

## Escenas

1. **Gancho (0 y 1):** Steve manda un libro abierto con "password: hunter2" por el camino; el vendedor lo lee en voz alta (globo).
2. **Las tres cosas (2 y 3):** sobre el camino aparecen tres objetos: cofre (privacidad), libro sellado (nada cambió) y etiqueta de nombre (con quién hablas).
3. **Saludo (4):** Steve y el banquero se saludan (globos "Hello! TLS 1.3").
4. **Certificado (5 a 7):** el banquero muestra la etiqueta "mybank.com" con brillo. Steve abre su libro de clérigos de confianza y el clérigo de la iglesia (CA) aparece con el mismo sello. El banquero firma (orbe/brillo) y un ladrón con una copia de la etiqueta no puede firmar.
5. **Pintura (8 a 13):** una mesa con lana amarilla en medio del camino (pública). Steve y el banquero mezclan en calderos: naranja y verde viajan por el camino; el espía mira; al final dos bloques de lana café, uno en cada lado.
6. **Cofres (14 a 16):** cofres cafés viajan por el camino; el espía solo ve cajas; uno que el espía intenta abrir se rompe y se tira.
7. **Candado (17 a 19):** un candado grande sobre la puerta del banco; luego el banco falso "myb4nk.com" también con candado, y Steve leyendo el nombre.
8. **Cierre (20):** repaso rápido y vuelta a la portada (loop).

## Decisiones de Claude

- Lugar nuevo: la llanura del sur de ClaudeEntorno (−168, 63, 152), aplanada para el camino.
- Reutiliza `gente.js`, `aldea.js` y el modo `solo3d`.
- Música: Subwoofer Lullaby (la favorita de Aldo).
