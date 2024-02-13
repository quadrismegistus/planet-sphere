// ipinfo.d.ts
declare module 'ipinfo' {
  interface IPInfo {
    ip: string;
    hostname?: string;
    city?: string;
    region?: string;
    country?: string;
    loc?: string; // latitude,longitude
    org?: string;
    postal?: string;
    timezone?: string;
  }

  interface IPInfoWrapper {
    (token: string, options?: object): {
      lookup(ip: string, callback: (err: Error, cinfo: IPInfo) => void): void;
    };
  }

  const ipinfo: IPInfoWrapper;
  export = ipinfo;
}
