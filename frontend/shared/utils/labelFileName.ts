export const toLabelSlug = (name: string) =>
    name.trim().replace(/[\s/\\:*?"<>|]+/g, "_") || "srodek";

export const toLabelFileName = (name: string, date?: string) =>
    `${toLabelSlug(name)}-etykieta${date ? `-${date}` : ""}.pdf`;
