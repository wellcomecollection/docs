// proposal for transformed eventDocument
// this is a "Parent" event with "Scheduled" events

const eventDocument = {
  id: 'ZcDCOhAAAPpnKL4S',
  display: {
    type: 'Event',
    id: 'ZcDCOhAAAPpnKL4S',
    title: 'The Beauty Sensorium Workshops',
    image: {
      type: 'PrismicImage',
      dimensions: { width: 4000, height: 2667 },
      alt: 'Photograph of a gallery visitor leaning over and smelling a large glass vessel within an installation. At the centre is multi-levelled podium covered in ornate coloured tiles. Suspended above are organically shaped glass vessels containing coloured liquid and natural substances. The wall behind in covered in renaissance images. The whole scene is dark but warmly lit.',
      copyright: 'Beauty Sensorium, 2023, Renaissance Goo x Baum & Leahy. Gallery Photo: Benjamin Gilbert | | Commissioned by Wellcome Collection | | CC-BY-NC | |',
      url: 'https://images.prismic.io/wellcomecollection/87ad8756-1e80-4b65-a1d3-6db0aef9a8cc_EP_002459_0015.jpg?auto=format,compress',
      id: 'ZUJuOxAAACMAq1IR',
      edit: { x: 0, y: 0, zoom: 1, background: '#fff' },
      '32:15': {
        dimensions: { width: 3200, height: 1500 },
        alt: 'Photograph of a gallery visitor leaning over and smelling a large glass vessel within an installation. At the centre is multi-levelled podium covered in ornate coloured tiles. Suspended above are organically shaped glass vessels containing coloured liquid and natural substances. The wall behind in covered in renaissance images. The whole scene is dark but warmly lit.',
        copyright: 'Beauty Sensorium, 2023, Renaissance Goo x Baum & Leahy. Gallery Photo: Benjamin Gilbert | | Commissioned by Wellcome Collection | | CC-BY-NC | |',
        url: 'https://images.prismic.io/wellcomecollection/87ad8756-1e80-4b65-a1d3-6db0aef9a8cc_EP_002459_0015.jpg?auto=format,compress',
        id: 'ZUJuOxAAACMAq1IR',
        edit: { x: 0, y: -317, zoom: 0.8, background: '#fff' }
      },
      '16:9': {
        dimensions: { width: 3200, height: 1800 },
        alt: 'Photograph of a gallery visitor leaning over and smelling a large glass vessel within an installation. At the centre is multi-levelled podium covered in ornate coloured tiles. Suspended above are organically shaped glass vessels containing coloured liquid and natural substances. The wall behind in covered in renaissance images. The whole scene is dark but warmly lit.',
        copyright: 'Beauty Sensorium, 2023, Renaissance Goo x Baum & Leahy. Gallery Photo: Benjamin Gilbert | | Commissioned by Wellcome Collection | | CC-BY-NC | |',
        url: 'https://images.prismic.io/wellcomecollection/87ad8756-1e80-4b65-a1d3-6db0aef9a8cc_EP_002459_0015.jpg?auto=format,compress',
        id: 'ZUJuOxAAACMAq1IR',
        edit: { x: 0, y: -167, zoom: 0.8, background: '#fff' }
      },
      square: {
        dimensions: { width: 3200, height: 3200 },
        alt: 'Photograph of a gallery visitor leaning over and smelling a large glass vessel within an installation. At the centre is multi-levelled podium covered in ornate coloured tiles. Suspended above are organically shaped glass vessels containing coloured liquid and natural substances. The wall behind in covered in renaissance images. The whole scene is dark but warmly lit.',
        copyright: 'Beauty Sensorium, 2023, Renaissance Goo x Baum & Leahy. Gallery Photo: Benjamin Gilbert | | Commissioned by Wellcome Collection | | CC-BY-NC | |',
        url: 'https://images.prismic.io/wellcomecollection/87ad8756-1e80-4b65-a1d3-6db0aef9a8cc_EP_002459_0015.jpg?auto=format,compress',
        id: 'ZUJuOxAAACMAq1IR',
        edit: { x: -800, y: 0, zoom: 1.1998500187476566, background: '#fff' }
      }
    },
    times: [
      {
        startDateTime: "2024-03-14T11:00:00.000Z",
        endDateTime: "2024-03-16T18:00:00.000Z",
        isFullyBooked: { inVenue: false, online: false }
      }
    ],
    format: { type: 'EventFormat', id: 'WcKmiysAACx_A8NR', label: 'Workshop' },
    locations: {
      type: 'EventLocations',
      isOnline: false,
      places: [
        {
          id: 'Wn3ZFyoAACkAIgPT',
          label: 'The Studio',
          type: 'EventPlace'
        }
      ],
      attendance: [
        {
          id: 'in-our-building',
          label: 'In our building',
          type: 'EventAttendance'
        }
      ]
    },
    interpretations: [
      {
        type: 'EventInterpretation',
        id: 'WmXhziQAACQAnw7i',
        label: 'Audio described'
      }
    ],
    audiences: [],
    series: [],
    isAvailableOnline: false
  },
  query: {
    linkedIdentifiers: [
      'WcKmiysAACx_A8NR',
      'Wn3ZFyoAACkAIgPT',
      'WmXhziQAACQAnw7i',
      'ZcDGvBAAACAAKMUC',
      'ZcDafhAAAB8AKOVa',
      'ZcDa4RAAAB8AKOZB',
      'ZcDbPxAAACAAKObo',
      'ZcDbshAAAB8AKOfO'
    ],
    title: 'The Beauty Sensorium Workshops',
    caption: 'Travel back in time to look, feel and smell the natural ingredients used in the cosmetic recipes of Renaissance Italy.',
    series: [],
    times: { startDateTime: [ "2024-03-14T11:00:00.000Z" ] }
  },
  // filter and aggregatableValues modified here to match the object they filters for/aggregate on, eg.
  // locationIds -> "locations.attendance" 
  // formatIDs -> format
  filter: {
    format: 'WcKmiysAACx_A8NR',
    "interpretations.label": [ 'Audio described' ], // if one/some of the Scheduled events had a different interpretation, it would be added here 
    audiences: [], // if one/some of the Scheduled events had a different target audience, it would be added here
    "locations.attendance": [ 'in-our-building' ], // if one/some of the Scheduled events was online, it would be added here
    isAvailableOnline: false, 
    // adding times filter
    "times.startDateTime": [ // times.startDateTime for every Scheduled event
      "2024-03-14T11:00:00.000Z",
      "2024-03-14T18:00:00.000Z",
      "2024-03-15T14:00:00.000Z",
      "2024-03-16T11:00:00.000Z",
      "2024-03-16T16:00:00.000Z",
    ]
  },
  aggregatableValues: {
    format: '{"type":"EventFormat","id":"WcKmiysAACx_A8NR","label":"Workshop"}',
    "interpretations.label": [
      '{"label":"Audio described","type":"InterpretationLabel"}'
    ],
    audiences: [],
    "locations.attendance": [
      '{"id":"in-our-building","label":"In our building","type":"EventAttendance"}'
    ],
    isAvailableOnline: '{"type":"OnlineAvailabilityBoolean","value":false,"label":"Catch-up event"}'
  }
}