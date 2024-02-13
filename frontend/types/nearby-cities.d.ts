declare module 'nearby-cities' {
  type CallbackFunction = () => void;
  type InitializeOptions = {
    level?: number;
    country?: string;
  };

  type Point = {
    lng?: number;
    latitude?: number;
    longitude?: number;
    lat?: number;
  };

  type City = {
    geonameid: string;
    name: string;
    asciiname: string;
    latitude: number;
    longitude: number;
    featureClass: string;
    featureCode: string;
    countryCode: string;
    cc2: string;
    admin1Code: string;
    admin2Code: string;
    admin3Code: string;
    admin4Code: string;
    population: number;
    elevation: number;
    dem: string;
    timezone: string;
    modificationDate: string;
  };

  type LocateResult = {
    nearest: City;
    distance: number;
    quadtree: string;
    log: string;
  } | null;

  export function initialize(callback: CallbackFunction, opts?: InitializeOptions): void;
  export function locate(point: Point): LocateResult;
}