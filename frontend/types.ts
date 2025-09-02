export type WikibaseJson = {
  id: string | number;
  urls: { baseUrl: string };
  wikibaseType?: string;
  description?: string;
  quantityObservations?: {
    mostRecent?: {
      observationDate?: string;
      totalItems?: number;
      totalProperties?: number;
      totalLexemes?: number;
      totalTriples?: number;
    };
  };
  recentChangesObservations?: {
    mostRecent?: {
      observationDate?: string;
      humanChangeCount?: number;
      humanChangeUserCount?: number;
      botChangeCount?: number;
      botChangeUserCount?: number;
    };
  };
  timeToFirstValueObservations?: {
    mostRecent?: {
      initiationDate?: string;
    };
  };
};

export type ObsKind = 'quantity' | 'rc';

export class Wikibase {
  id: string | number;
  urls: { baseUrl: string };
  wikibaseType?: string;
  description?: string;
  quantityObservations?: WikibaseJson['quantityObservations'];
  recentChangesObservations?: WikibaseJson['recentChangesObservations'];
  timeToFirstValueObservations?: WikibaseJson['timeToFirstValueObservations'];

  private static nf = new Intl.NumberFormat(undefined);

  constructor(data: WikibaseJson) {
    this.id = data.id;
    this.urls = data.urls;
    this.wikibaseType = data.wikibaseType;
    this.description = data.description;
    this.quantityObservations = data.quantityObservations;
    this.recentChangesObservations = data.recentChangesObservations;
    this.timeToFirstValueObservations = data.timeToFirstValueObservations;
  }

  static from(data: WikibaseJson): Wikibase {
    return new Wikibase(data);
  }

  baseHost(): string {
    const url = this.urls?.baseUrl;
    if (!url) return '';
    try {
      const u = new URL(url);
      return u.host + u.pathname;
    } catch {
      return url;
    }
  }

  fmt(n?: number | null): string {
    if (n == null) return '';
    try {
      return Wikibase.nf.format(n as number);
    } catch {
      return String(n);
    }
  }

  fmtDate(s?: string): string {
    if (!s) return '';
    const d = new Date(s);
    return Number.isNaN(d.getTime()) ? s : d.toLocaleDateString();
  }

  hasQuantity(): boolean {
    const m = this.quantityObservations?.mostRecent;
    if (!m) return false;
    const vals = [m.totalItems, m.totalProperties, m.totalLexemes, m.totalTriples];
    return vals.some((v) => typeof v === 'number' && v > 0);
  }

  hasRecentChanges(): boolean {
    const m = this.recentChangesObservations?.mostRecent;
    if (!m) return false;
    const vals = [
      m.humanChangeCount,
      m.humanChangeUserCount,
      m.botChangeCount,
      m.botChangeUserCount,
    ];
    return vals.some((v) => typeof v === 'number' && v > 0);
  }

  getObservationDate(kind: ObsKind): string | undefined {
    return kind === 'quantity'
      ? this.quantityObservations?.mostRecent?.observationDate
      : this.recentChangesObservations?.mostRecent?.observationDate;
  }

  // Intentionally no obsHeadlineSuffix here; UI concerns live in the card component.
}
