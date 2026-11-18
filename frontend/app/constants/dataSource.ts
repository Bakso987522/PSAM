export const DATA_SOURCE_URL = (datasetId: string) =>
    datasetId
        ? `https://dane.gov.pl/pl/dataset/${encodeURIComponent(datasetId)}`
        : "https://dane.gov.pl";
