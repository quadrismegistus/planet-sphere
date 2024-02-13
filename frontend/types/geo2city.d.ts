// geo2city.d.ts
declare module 'geo2city' {
  type Latitude = number;
  type Longitude = number;
  type Coordinates = [Latitude, Longitude];

  interface GeoData {
    latitude: Latitude;
    longitude: Longitude;
    iso2: string;
    iso3: string;
    flag: string;
    country: string;
    city: string;
  }

  /**
   * Given an array of latitude and longitude numbers, returns city related data,
   * if any, or undefined.
   * @param coordinates - coordinates to reverse geocode
   * @returns A Promise resolved with GeoData or undefined
   */
  export function reverse(coordinates: Coordinates): Promise<GeoData | void>;

  /**
   * Given a generic search string, optionally comma separated, returns the
   * nearest city coordinates, if any, or undefined.
   * @param search - string to retrieve the nearest city coordinates
   * @returns A Promise resolved with Coordinates or undefined
   */
  export function search(search: string): Promise<Coordinates | void>;

  /**
   * Given a generic IPv4 address, returns city related data, if any,
   * or undefined.
   * @param IPv4 - address to search via geoiplookup
   * @returns A Promise resolved with Coordinates or undefined
   */
  export function ip(IPv4: string): Promise<Coordinates | void>;
}
