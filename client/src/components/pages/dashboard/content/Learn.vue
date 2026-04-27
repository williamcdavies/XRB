<script setup lang="ts">
import { ref } from 'vue'

const activeSection = ref<'lrlx' | 'xrb'>('lrlx')
</script>

<template>
  <div class="flex-1 flex flex-col min-h-0 min-w-0 overflow-hidden bg-xrb-bg-1 text-xrb-text-primary">

    <!-- Header -->
    <!-- <div class="flex items-center justify-between px-6 py-4 border-b border-xrb-border bg-xrb-bg-2 shrink-0">
      <h2 class="text-sm tracking-widest uppercase">Learn</h2>
    </div> -->

    <!-- Scrollable content -->
    <div class="flex-1 overflow-y-auto">

      <!-- Hero -->
      <div class="relative overflow-hidden">
        <img
          src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Black_hole_-_Messier_87_crop_max_res.jpg/1280px-Black_hole_-_Messier_87_crop_max_res.jpg"
          alt="First image of a black hole, Messier 87"
          class="w-full h-72 object-cover object-center opacity-60"
        />
        <div class="absolute inset-0 bg-gradient-to-b from-transparent via-black/40 to-xrb-bg-1"></div>
        <div class="absolute bottom-0 left-0 right-0 px-8 pb-8 text-xrb-text-primary">
          <h1 class="text-4xl font-bold leading-tight text-center">Accreting Black Holes</h1>
          <div class="flex mx-auto max-w-4xl mt-4 border-b border-xrb-text-secondary/25"></div>
          <p class="italic text-lg text-xrb-text-primary text-center mt-4 mx-auto max-w-4xl">
            Some black holes have a companion star. Over time, they steal gas from it. That gas glows brilliantly
            in X-rays as it spirals inward. Let's take a deep dive into the data behind those systems.
          </p>
          <p class="text-xs text-xrb-text-secondary text-right mt-10 opacity-60">
            Image credit: Event Horizon Telescope Collaboration, CC BY 4.0. First-ever photograph of a black hole (M87*, 2019)
          </p>
        </div>
      </div>

      <!-- Intro -->
      <div class="flex mx-auto justify-center px-8 py-6 max-w-4xl text-xrb-text-primary">
        <div class="rounded-xl p-5">
          <h3 class="text-xl font-semibold tracking-wide text-xrb-accent mb-2">Overview: What is an X-Ray Binary?</h3>
          <p class="text-lg text-xrb-text-secondary leading-relaxed">
            An <strong class="text-xrb-accent-1">X-Ray Binary (XRB)</strong> is a two-star system where one object is
            a <strong class="text-xrb-accent-1">black hole</strong> (or neutron star) and the other is an ordinary
            companion star. The black hole's gravity pulls material off the companion. That material forms a swirling
            disk — called an <strong class="text-xrb-accent-1">accretion disk</strong> — that heats up to millions of
            degrees and shines brightly in X-rays. By measuring the radio and X-ray light from these systems,
            scientists can learn about the black hole's mass, distance, and how efficiently it converts matter into energy.
          </p>
        </div>
      </div>

      <!-- Section tab switcher -->
      <div class="flex mx-auto justify-center px-8 py-8">
        <div class="flex gap-2 border-b border-xrb-border">
          <button
            class="px-4 py-2 text-sm tracking-wide transition-colors"
            :class="activeSection === 'lrlx'
              ? 'text-xrb-accent border-b-2 border-xrb-accent font-semibold'
              : 'text-xrb-text-secondary hover:text-xrb-text-primary'"
            @click="activeSection = 'lrlx'"
          >
            Radio–X-ray Correlation (L<sub>R</sub>–L<sub>X</sub>)
          </button>
          <button
            class="px-4 py-2 text-sm tracking-wide transition-colors"
            :class="activeSection === 'xrb'
              ? 'text-xrb-accent border-b-2 border-xrb-accent font-semibold'
              : 'text-xrb-text-secondary hover:text-xrb-text-primary'"
            @click="activeSection = 'xrb'"
          >
            XRB System Properties
          </button>
        </div>
      </div>

      <!-- ── LRLX SECTION ── -->
      <div v-if="activeSection === 'lrlx'" class="px-8 py-6 max-w-4xl space-y-6 flex flex-col mx-auto justify-center">

        <div>
          <h2 class="text-xl font-bold text-xrb-text-primary mb-1">The Radio–X-ray Luminosity Correlation</h2>
          <p class="text-lg text-xrb-text-secondary leading-relaxed">
            One of the most important discoveries in black hole physics is that <strong class="text-xrb-text-primary">radio brightness
            and X-ray brightness track each other</strong>. When a black hole accretes more material,
            both its X-ray glow (from the hot disk) and its radio jet (a beam of fast-moving particles) get brighter together.
            This tight relationship — called the <em>fundamental plane of black hole accretion</em> — holds across stellar-mass
            black holes in our galaxy and even supermassive black holes in distant galaxies.
          </p>
        </div>

        <!-- Property cards -->
        <h3 class="text-xl text-xrb-accent-1 font-semibold tracking-widest uppercase text-xrb-accent">L<sub>R</sub>–L<sub>X</sub> Data Columns Explained</h3>

        <div class="grid grid-cols-1 gap-4">

          <div class="rounded-xl p-5">
            <div class="flex items-start gap-3">
              <div>
                <h4 class="font-semibold text-xrb-text-primary text-xl mb-3">
                  L<sub>R</sub> — Radio Luminosity
                </h4>
                <p class="text-lg text-xrb-text-secondary leading-relaxed">
                  <strong class="text-xrb-text-primary">Luminosity</strong> means total power output — how much energy
                  something radiates per second. L<sub>R</sub> is the power output in
                  <strong class="text-xrb-text-primary">radio waves</strong>, measured in ergs per second (erg/s).
                  For comparison, the Sun puts out about 4 × 10<sup>33</sup> erg/s — these black holes can be
                  trillions of times more powerful in radio alone. Radio emission in black hole X-ray binaries
                  is thought to come from a <em>relativistic jet</em> — a narrow beam of plasma
                  launched near the black hole at nearly the speed of light.
                </p>
              </div>
            </div>
          </div>

          <div class="rounded-xl p-5">
            <div class="flex items-start gap-3">
              <div>
                <h4 class="font-semibold text-xrb-text-primary text-xl mb-1">
                  L<sub>R_ler</sub>L<sub>R_uer</sub> — Radio Luminosity Error Bounds
                </h4>
                <p class="text-lg text-xrb-text-secondary leading-relaxed">
                  Scientific measurements always come with <strong class="text-xrb-text-primary">uncertainty</strong>.
                  <em>L<sub>R_ler</sub></em> is the <strong class="text-xrb-text-primary">lower error</strong>
                  (how much lower the true value could be) and
                  <em>L<sub>R_uer</sub></em> is the <strong class="text-xrb-text-primary">upper error</strong>
                  (how much higher it could be). When these values are <em>inf</em> (infinity), it means the
                  measurement has no reliable upper or lower bound — perhaps because the source was only
                  detected at a single snapshot in time, or because the distance to the system is not well-constrained.
                  Error bars are not a sign of bad data; they honestly communicate what we know and don't know.
                </p>
              </div>
            </div>
          </div>

          <div class="rounded-xl p-5">
            <div class="flex items-start gap-3">
              <div>
                <h4 class="font-semibold text-xrb-text-primary text-xl mb-1">
                  L<sub>X</sub> — X-ray Luminosity
                </h4>
                <p class="text-lg text-xrb-text-secondary leading-relaxed">
                  L<sub>X</sub> is the power output in <strong class="text-xrb-text-primary">X-rays</strong>.
                  This light comes from the innermost, hottest part of the accretion disk and a corona
                  of energetic particles above it. X-rays are invisible to our eyes and blocked by Earth's
                  atmosphere, so they must be observed from space telescopes like
                  <em>Chandra</em>, <em>XMM-Newton</em>, and <em>RXTE</em>.
                  L<sub>X</sub> values here are typically in the range 10<sup>30</sup>–10<sup>35</sup> erg/s,
                  meaning these systems are among the brightest X-ray sources in our entire galaxy.
                </p>
              </div>
            </div>
          </div>

          <div class="rounded-xl p-5">
            <div class="flex items-start gap-3">
              <div>
                <h4 class="font-semibold text-xrb-text-primary text-xl mb-1">
                  L<sub>X_ler</sub> &amp; L<sub>X_uer</sub> — X-ray Luminosity Error Bounds
                </h4>
                <p class="text-lg text-xrb-text-secondary leading-relaxed">
                  Same concept as the radio errors — lower and upper uncertainty on L<sub>X</sub>.
                  These arise from uncertainty in the <strong class="text-xrb-text-primary">source distance</strong>
                  (luminosity scales as distance squared, so a 10% distance error causes a ~20% luminosity error),
                  calibration uncertainties in the telescope, and the assumed spectral model used to convert
                  raw counts into physical flux.
                </p>
              </div>
            </div>
          </div>

          <div class="rounded-xl p-5">
            <div class="flex items-start gap-3">
              <div>
                <h4 class="font-semibold text-xrb-text-primary text-xl mb-1">
                  uplim — Upper Limit Flag
                </h4>
                <p class="text-lg text-xrb-text-secondary leading-relaxed">
                  When the <code class="bg-xrb-bg-1 px-1 rounded text-xs">uplim</code> column is not NULL,
                  it signals that the measured value is an <strong class="text-xrb-text-primary">upper limit</strong>
                  rather than a real detection. This means the telescope could not clearly detect the source —
                  it only knows the source is <em>at most</em> this bright. Upper limits are common in
                  quiescent (quiet) black holes that have nearly stopped accreting. Plotting them correctly
                  (as arrows pointing down on a log-log diagram) is crucial for honest science.
                </p>
              </div>
            </div>
          </div>

          <div class="rounded-xl p-5">
            <div class="flex items-start gap-3">
              <div>
                <h4 class="font-semibold text-xrb-text-primary text-xl mb-1">
                  alpha — Spectral Index
                </h4>
                <p class="text-lg text-xrb-text-secondary leading-relaxed">
                  The <strong class="text-xrb-text-primary">spectral index</strong> (α) describes
                  <em>how the radio brightness changes with frequency</em>. A value of
                  <strong class="text-xrb-text-primary">α = 0</strong> means a flat spectrum —
                  the source emits equally across radio frequencies. This is the classic signature
                  of a <em>compact, self-absorbed jet</em> in the hard state of a black hole X-ray binary.
                  Steeper values indicate optically thin emission or a different emission mechanism.
                </p>
              </div>
            </div>
          </div>

          <div class="rounded-xl p-5">
            <div class="flex items-start gap-3">
              <div>
                <h4 class="font-semibold text-xrb-text-primary text-xl mb-1">
                  nu — Observed Frequency (GHz)
                </h4>
                <p class="text-lg text-xrb-text-secondary leading-relaxed">
                  <strong class="text-xrb-text-primary">nu (ν)</strong> is the radio frequency at which
                  the observation was made, in gigahertz (GHz). Most of these measurements use
                  5 GHz, a standard band used by radio telescopes like the
                  <em>Very Large Array (VLA)</em> in New Mexico. The choice of frequency affects
                  the measured flux, which is why the spectral index α is needed to convert to a
                  standard reference frequency for fair comparison between different systems.
                </p>
              </div>
            </div>
          </div>

          <div class="rounded-xl p-5">
            <div class="flex items-start gap-3">
              <div>
                <h4 class="font-semibold text-xrb-text-primary text-xl mb-1">
                  E_1measured &amp; E_2measured — X-ray Energy Band (keV)
                </h4>
                <p class="text-lg text-xrb-text-secondary leading-relaxed">
                  These define the <strong class="text-xrb-text-primary">energy band</strong> of the
                  X-ray observation — the lowest (E_1) and highest (E_2) photon energies included,
                  measured in <em>kiloelectronvolts (keV)</em>. A 1–10 keV band is a typical
                  "soft X-ray" window. Different telescopes cover different energy ranges,
                  and all fluxes must be converted to a common band to make
                  cross-system comparisons valid. Think of it like comparing brightness between
                  photos taken with different camera filters — you need to account for the filter first.
                </p>
              </div>
            </div>
          </div>

          <div class="rounded-xl p-5">
            <div class="flex items-start gap-3">
              <div>
                <h4 class="font-semibold text-xrb-text-primary text-xl mb-1">
                  gamma — Photon Index
                </h4>
                <p class="text-lg text-xrb-text-secondary leading-relaxed">
                  The <strong class="text-xrb-text-primary">photon index</strong> (Γ) describes
                  the shape of the X-ray energy spectrum — how many photons arrive at each energy.
                  A value of <strong class="text-xrb-text-primary">Γ = 1.7</strong> is typical for
                  black holes in the <em>hard spectral state</em>, where accretion is low and
                  the emission is dominated by a hot corona of electrons that Compton-scatter
                  photons to higher energies. It's used to convert the measured X-ray flux into
                  a consistent luminosity across the standard energy band.
                </p>
              </div>
            </div>
          </div>

          <div class="rounded-xl p-5">
            <div class="flex items-start gap-3">
              <div>
                <h4 class="font-semibold text-xrb-text-primary text-xl mb-1">
                  time — Time Offset Between Observations (days)
                </h4>
                <p class="text-lg text-xrb-text-secondary leading-relaxed">
                  Black hole X-ray binaries can change dramatically within hours or days.
                  The <strong class="text-xrb-text-primary">time column</strong> records the
                  time difference (in days) between the radio and X-ray observations used
                  for a single data point. A value of <strong class="text-xrb-text-primary">0.0</strong>
                  means the two measurements were simultaneous — the ideal case.
                  Large offsets can introduce scatter into the correlation because the source
                  may have brightened or faded between the two observations.
                </p>
              </div>
            </div>
          </div>

          <div class="rounded-xl p-5">
            <div class="flex items-start gap-3">
              <div>
                <h4 class="font-semibold text-xrb-text-primary text-xl mb-1">
                  Ref — Reference Publication
                </h4>
                <p class="text-lg text-xrb-text-secondary leading-relaxed">
                  Every data point in science traces back to a published paper.
                  The <strong class="text-xrb-text-primary">Ref column</strong> lists the
                  journal articles (e.g., MNRAS = Monthly Notices of the Royal Astronomical Society,
                  ApJ = Astrophysical Journal) where the original observations were reported.
                  Citing sources allows other scientists to verify, reproduce, or build on the work —
                  a cornerstone of the scientific process.
                </p>
              </div>
            </div>
          </div>

        </div>
      </div>

      <!-- ── XRB SECTION ── -->
      <div v-if="activeSection === 'xrb'" class="flex-col mx-auto justify-center px-8 py-6 max-w-4xl space-y-6">

        <div>
          <h2 class="text-xl font-bold text-xrb-text-primary mb-1">X-Ray Binary System Properties</h2>
          <p class="text-lg text-xrb-text-secondary leading-relaxed">
            To use the radio–X-ray correlation, we need to know the physical properties of each black hole system.
            This table records characteristics like how far away the system is, how it's tilted, and how massive
            the black hole is — all of which are needed to convert raw telescope data into physical luminosities.
          </p>
        </div>

        <h3 class="text-xl text-xrb-accent-1 font-semibold tracking-widest uppercase text-xrb-accent">System Data Columns Explained</h3>

        <div class="grid grid-cols-1 gap-4">

          <div class="p-5">
            <div class="flex items-start gap-3">
              <div>
                <h4 class="font-semibold text-xrb-text-primary text-xl mb-3">Name</h4>
                <p class="text-lg text-xrb-text-secondary leading-relaxed">
                  The <strong class="text-xrb-text-primary">catalog name</strong> of the X-ray binary system.
                  Many names reflect the telescope or survey that discovered them. For example,
                  <em>GRO J1655-40</em> was found by the <em>Compton Gamma Ray Observatory (GRO)</em>,
                  while its position on the sky is encoded as J1655-40 (right ascension and declination
                  in the J2000 coordinate epoch). Names like <em>4U 1543-47</em> come from the
                  <em>Uhuru</em> satellite, the first X-ray astronomy mission.
                </p>
              </div>
            </div>
          </div>

          <div class="p-5">
            <div class="flex items-start gap-3">
              <div>
                <h4 class="font-semibold text-xrb-text-primary text-xl mb-3">Dist &amp; DistErr: Distance (kpc)</h4>
                <p class="text-lg text-xrb-text-secondary leading-relaxed">
                  <strong class="text-xrb-text-primary">Dist</strong> is the distance to the system in
                  <strong class="text-xrb-text-primary">kiloparsecs (kpc)</strong>.
                  One kiloparsec equals about 3,260 light-years. So, a distance of 8.4 kpc (like GX 339-4)
                  means the system is roughly 27,000 light-years away, near the center of our galaxy.
                  <strong class="text-xrb-text-primary">DistErr</strong> is the uncertainty on this distance.
                  Distance is the single most important number for converting observed flux into true luminosity,
                  since luminosity = 4π × distance² × flux.
                </p>
              </div>
            </div>
          </div>

          <div class="p-5">
            <div class="flex items-start gap-3">
              <div>
                <h4 class="font-semibold text-xrb-text-primary text-xl mb-3">RL: Radio-Loud / Radio-Quiet Classification</h4>
                <p class="text-lg text-xrb-text-secondary leading-relaxed">
                  Black hole X-ray binaries are divided into two populations based on how much radio
                  emission they produce relative to their X-rays.
                  <strong class="text-xrb-text-primary">RL (Radio-Loud)</strong> sources like 4U 1543-47
                  and GX 339-4 follow the standard correlation track and have bright jets.
                  <strong class="text-xrb-text-primary">RQ (Radio-Quiet)</strong> sources like GRO J1655-40
                  are systematically fainter in radio for the same X-ray brightness, possibly because their
                  jet is suppressed or pointed away from us. Understanding why this split exists is
                  an active research question.
                </p>
              </div>
            </div>
          </div>

          <div class="p-5">
            <div class="flex items-start gap-3">
              <div>
                <h4 class="font-semibold text-xrb-text-primary text-xl mb-3">Incl &amp; InclErr — Orbital Inclination (°)</h4>
                <p class="text-lg text-xrb-text-secondary leading-relaxed">
                  <strong class="text-xrb-text-primary">Inclination</strong> is the tilt of the binary orbit
                  relative to our line of sight, measured in degrees.
                  At <strong class="text-xrb-text-primary">0°</strong>, we'd look straight down onto the
                  orbital plane (face-on). At <strong class="text-xrb-text-primary">90°</strong>, we see the
                  orbit edge-on. Inclination matters because it affects how we measure the
                  companion star's radial velocity — which is used to determine the black hole's mass.
                  High inclinations also mean the system can produce <em>X-ray eclipses</em> or dips
                  as the companion passes in front of the accretion disk.
                </p>
              </div>
            </div>
          </div>

          <div class="p-5">
            <div class="flex items-start gap-3">
              <div>
                <h4 class="font-semibold text-xrb-text-primary text-xl mb-3">HardlineSlope &amp; HardlineSlopeErr</h4>
                <p class="text-lg text-xrb-text-secondary leading-relaxed">
                  On a log–log plot of radio vs. X-ray luminosity, each black hole system traces a
                  <em>hard-state track</em> — a power-law line called the
                  <strong class="text-xrb-text-primary">hard-line</strong>.
                  <strong class="text-xrb-text-primary">HardlineSlope</strong> is the slope of that line
                  for the individual source. The canonical slope from early studies was ~0.6,
                  but individual systems range from ~0.9 to ~1.4, reflecting differences in jet physics
                  and disk–jet coupling. The uncertainty on this slope is captured in
                  <strong class="text-xrb-text-primary">HardlineSlopeErr</strong>.
                </p>
              </div>
            </div>
          </div>

          <div class="p-5">
            <div class="flex items-start gap-3">
              <div>
                <h4 class="font-semibold text-xrb-text-primary text-xl mb-3">SpecType — Companion Star Spectral Type</h4>
                <p class="text-lg text-xrb-text-secondary leading-relaxed">
                  Every X-ray binary has a normal companion star. Its
                  <strong class="text-xrb-text-primary">spectral type</strong> tells us the star's temperature
                  and size, using the standard astronomical classification (O, B, A, F, G, K, M —
                  hot to cool). <em>A2V</em> (like in 4U 1543-47) is a hot, white A-type main-sequence star.
                  <em>F6IV</em> (GRO J1655-40) is a slightly evolved subgiant, slightly cooler and larger
                  than our Sun. The spectral type determines how much mass the companion is likely to donate
                  and how long the system will stay active.
                </p>
              </div>
            </div>
          </div>

          <div class="p-5">
            <div class="flex items-start gap-3">
              <div>
                <h4 class="font-semibold text-xrb-text-primary text-xl mb-3">Porb — Orbital Period (hours)</h4>
                <p class="text-lg text-xrb-text-secondary leading-relaxed">
                  <strong class="text-xrb-text-primary">Porb</strong> is how long it takes the two stars
                  to complete one orbit around each other, in hours.
                  GRO J1655-40 has an orbital period of about 62.9 hours (~2.6 days), while
                  4U 1543-47 takes about 26.8 hours. Using Kepler's laws, the orbital period combined
                  with the radial velocity of the companion star lets astronomers weigh the
                  black hole — one of the only ways to confirm an object is truly a black hole
                  (rather than a neutron star) from Earth.
                </p>
              </div>
            </div>
          </div>

          <div class="p-5">
            <div class="flex items-start gap-3">
              <div>
                <h4 class="font-semibold text-xrb-text-primary text-xl mb-3">Mass — Black Hole Mass (M☉)</h4>
                <p class="text-lg text-xrb-text-secondary leading-relaxed">
                  <strong class="text-xrb-text-primary">Mass</strong> is the black hole's mass in units of
                  <strong class="text-xrb-text-primary">solar masses (M☉)</strong> — multiples of our Sun's mass.
                  The systems in this dataset range from about 6 to over 10 solar masses. To put that
                  in perspective, our Sun would have to be crushed to a sphere about 3 km across to become
                  a black hole of 1 M☉. A value of <em>&gt;6</em> means the mass is a lower limit —
                  confirming it's definitely a black hole (neutron stars cannot exceed ~3 M☉),
                  even if the exact mass isn't pinned down yet.
                </p>
              </div>
            </div>
          </div>

        </div>

        <!-- Footer callout -->
        <div class="p-5">
          <h4 class="italic text-xl text-xrb-accent-1 mb-2">Why Does This All Matter?</h4>
          <p class="text-lg text-xrb-text-secondary leading-relaxed">
            By combining all of these properties — distance, inclination, mass, orbital period, jet slope,
            and spectral data — astronomers can test fundamental physics: how does matter behave at the
            edge of a black hole? How efficiently is gravitational energy converted to light and jets?
            Do all black holes follow the same universal rules, or do individual properties like spin
            and mass create diversity? The XRB dataset compiled here is one of the primary tools used
            to answer these questions.
          </p>
        </div>

      </div>

      <!-- Bottom padding -->
      <div class="h-12"></div>

    </div>
  </div>
</template>

<style scoped>
</style>