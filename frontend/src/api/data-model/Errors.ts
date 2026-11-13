

export class APIResponseError extends Error {
  constructor(message: string) {
    super(message);
  }
}