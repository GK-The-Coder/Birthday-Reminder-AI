import test from "node:test";
import assert from "node:assert/strict";
import { getApiErrorMessage } from "./apiErrors.js";

test("uses the API detail when available", () => {
  assert.equal(
    getApiErrorMessage({ response: { data: { detail: "Email failed" } } }),
    "Email failed",
  );
});

test("falls back to the error message", () => {
  assert.equal(getApiErrorMessage({ message: "Network unavailable" }), "Network unavailable");
});

test("uses the default message when no details exist", () => {
  assert.equal(getApiErrorMessage({}, "Try again"), "Try again");
});