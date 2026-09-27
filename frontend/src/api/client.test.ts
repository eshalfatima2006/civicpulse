import { afterEach, describe, expect, it, vi } from "vitest";

import { postComplaint } from "./client";

afterEach(() => vi.restoreAllMocks());

describe("postComplaint", () => {
  it("posts a complaint to the API and returns the typed response", async () => {
    const complaint = { id: "complaint-1", category: "roads", priority: "normal" };
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify(complaint), { status: 201 }),
    );

    const payload = { text: "There is a large pothole", location: "Main Street" };
    const result = await postComplaint(payload);

    expect(fetchMock).toHaveBeenCalledWith("/api/complaints", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    expect(result).toEqual(complaint);
  });
});
